#!/bin/sh

port=$2
if [ "$port" = "" ]; then
    port=8101
fi

if [ $1 = "app" ]; then
    echo "start app"
    /usr/local/bin/python -m gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$port
fi