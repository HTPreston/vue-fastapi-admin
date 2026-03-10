"""Custom Celery worker pool."""

# Future Imports
from __future__ import annotations

# Standard Library Imports
import asyncio as aio
import inspect
import os
import threading
import typing

AnyCallable = typing.Callable[..., typing.Any]
AnyException = typing.Union[Exception, typing.Type[Exception]]
AnyCoroutine = typing.Coroutine[typing.Any, typing.Any, typing.Any]

__all__ = ("AsyncIOPool",)


class AsyncIOPool:
    loop: aio.AbstractEventLoop
    loop_runner: threading.Thread
    singleton: typing.Optional["AsyncIOPool"] = None

    def __new__(cls, *args: typing.Any, **kwargs: typing.Any) -> "AsyncIOPool":

        # Because the worker pool uses an instance-bound thread
        # to run its asyncio eventloop, it's a good idea to ensure
        # that there can't be more than one instance of the pool
        # created per process

        if not isinstance(cls.singleton, cls):
            cls.singleton = super(AsyncIOPool, cls).__new__(cls)

        # Return the class-bound worker pool instance
        return cls.singleton

    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:

        # If there is already a running asyncio event loop
        # in the current thread / process, it's not a great
        # idea to allow the worker pool to create another
        # and the `AsyncIOPool` can't function at all without
        # one, so we'll throw a `SystemError` if one is detected
        # as a way to short-circuit the worker start up process
        try:
            aio.get_running_loop()
            raise SystemError("There is already a running event loop in this thread!")
        except RuntimeError:
            pass

        # Regardless of what the user specifies in the local
        # configuration, `threads` and `forking_enable` should
        # *always* be False when using `AsyncIOPool` as the
        # worker pool class, so we'll set them forcibly here

        kwargs.update(
            threads=False,
            forking_enable=False,
        )

        # ... perform the usual "housekeeping", ...
        self.limit = 1

        # ... create the pool's asyncio eventloop ...
        self.loop = aio.new_event_loop()

        # ... and let it run in an instance-bound thread.
        self.loop_runner = threading.Thread(
            target=self.loop.run_forever,
            name="celery-worker-async-loop",
            daemon=True,
        )

        self.loop_runner.start()

        # Set the new event loop as the "active" eventloop
        # in current thread / process
        aio.set_event_loop(self.loop)

    def run(
            self,
            task_function: AnyCallable | AnyCoroutine,
            *args: typing.Any,
            **kwargs: typing.Any,
    ) -> typing.Any:
        """Run the supplied coroutine in the pool's bound loop-runner
        thread."""

        # If the supplied function is actually an async function
        # (i.e. async def some_function() -> Any), call it with
        # the supplied arguments and bind the returned coroutine
        # so we can run it on the worker's thread-bound eventloop
        if inspect.iscoroutinefunction(task_function):
            task_function = task_function(*args, **kwargs)

        # If the supplied function is actually a vanilla Python
        # function (i.e. def any_function() -> Any), use asyncio's
        # `to_thread` utility to wrap it along the supplied arguments
        # and bind the returned coroutine so we can run it on the
        # worker's thread-bound eventloop
        if callable(task_function) and not bool(
                inspect.iscoroutine(task_function) or aio.isfuture(task_function)
        ):
            task_function = aio.to_thread(
                task_function,
                *args,
                **kwargs,
            )

        # If the value of `task_function` isn't actually something
        # that can be awaited (i.e. run on an async eventloop),
        # return it as it's either the actual result of having
        # called and run `task_function` -or- it's something we
        # can't meaningfully do anything with anyway
        if not inspect.isawaitable(task_function):
            return task_function

        # At this point, we're guaranteed to have something
        # that's either an actual coroutine or some other kind
        # of `asyncio.Future` which means we need to throw it
        # onto the worker's thread-bound eventloop to be run
        try:
            result: aio.Future = aio.run_coroutine_threadsafe(
                task_function,
                self.loop,
            )
        except TypeError:
            return task_function

        # Once the our future has been awaited, it will either
        # have raised an exception or returned a result. If it
        # raised an exception, propagate it back to the caller
        if error := result.exception():
            raise error

        # If no exception was raised, pass `.result()` back through
        # `AsyncIOPool.run` so that it can be checked to ensure it's
        # properly handled in case another callable or awaitable was
        # returned
        return self.run(result.result())

    @classmethod
    def run_in_pool(
            cls,
            task_function: AnyCallable | AnyCoroutine,
            *args: typing.Any,
            **kwargs: typing.Any,
    ) -> typing.Any:
        """Run the supplied task in the pool's thread-bound async loop."""
        if not (worker_pool := cls.singleton):
            worker_pool = cls()

        return worker_pool.run(
            task_function,
            *args,
            **kwargs,
        )

    async def shutdown(self) -> None:
        """Shut down the worker pool."""
        if self.loop.is_running():
            self.loop.stop()
            await self.loop.shutdown_asyncgens()

        if not self.loop.is_closed() and callable(
                (
                        closer := getattr(
                            self.loop,
                            "aclose",
                            None,
                        )
                )
        ):
            await closer()

    def join(self) -> None:
        """Join the loop-runner thread."""
        self.loop_runner.join()

