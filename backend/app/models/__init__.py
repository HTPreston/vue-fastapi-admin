# -*- coding: utf-8 -*-
# @author: xiaobai
import asyncio

from loguru import logger
from app.db.sqlalchemy import engine
from app.models.base import Base

# 导入所有模型以确保表被注册到 Base.metadata
from app.models.system_models import UserLoginRecord


# async def init_single_table(table_name: str):
#     """
#     初始化单个数据库表

#     只创建指定的表，不影响其他已存在的表。
#     如果表已存在，会先删除再重新创建。

#     :param table_name: 表名
#     :type table_name: str
#     :return: None
#     """
#     from sqlalchemy import inspect

#     async with engine.begin() as conn:
#         # 检查表是否存在
#         def check_table_exists(connection):
#             inspector = inspect(connection)
#             return table_name in inspector.get_table_names()

#         table_exists = await conn.run_sync(check_table_exists)

#         if table_exists:
#             logger.info(f"表 {table_name} 已存在，正在删除...")
#             # 获取指定表的 Table 对象并删除
#             table = Base.metadata.tables.get(table_name)
#             if table is not None:
#                 await conn.run_sync(table.drop)
#                 logger.info(f"表 {table_name} 已删除")

#         # 创建指定表
#         table = Base.metadata.tables.get(table_name)
#         if table is not None:
#             await conn.run_sync(table.create)
#             logger.info(f"表 {table_name} 创建完成！")
#         else:
#             logger.error(f"表 {table_name} 在模型中未找到！")
