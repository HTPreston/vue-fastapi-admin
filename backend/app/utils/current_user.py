# -*- coding: utf-8 -*-
# @author: xiaobai
import typing

from app.corelibs.consts import TEST_USER_INFO
from app.db import redis_pool
from app.exceptions.exceptions import AccessTokenFail
from app.utils.context import AccessToken


async def current_user(token: str = None) -> typing.Union[typing.Dict[typing.Text, typing.Any], None]:
    """根据token获取用户信息"""
    import json
    import ast
    user_info = await redis_pool.redis.get(TEST_USER_INFO.format(AccessToken.get() if not token else token))
    if not user_info:
        raise AccessTokenFail()
    # 确保返回的是字典对象
    if isinstance(user_info, str):
        try:
            # 尝试解析 JSON
            return json.loads(user_info)
        except Exception:
            # 尝试处理双重转义的 JSON 字符串
            try:
                # 先解码一次
                unescaped = user_info.replace('\\"', '"')
                return json.loads(unescaped)
            except Exception:
                # 再次尝试处理
                try:
                    # 可能需要多次解码
                    return ast.literal_eval(user_info)
                except Exception:
                    raise AccessTokenFail()
    return user_info
