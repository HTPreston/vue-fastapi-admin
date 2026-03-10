# -*- coding: utf-8 -*-
# @author: xiaobai
from datetime import datetime
import typing
from fastapi.encoders import jsonable_encoder
from sqlalchemy import Select, select, func, literal_column, Row
from sqlalchemy.orm import noload, DeclarativeMeta

T = typing.TypeVar("T", Select, "Query[Any]")


def count_query(query: Select) -> Select:
    """
    获取count sql
    :param query: sql
    :return:
    """
    count_subquery = typing.cast(typing.Any, query.order_by(None)).options(noload("*")) .subquery()
    return select(func.count(literal_column("*"))).select_from(count_subquery)


def paginate_query(query: T, page: int, page_size: int) -> T:
    """
    获取分页sql
    :param query:
    :param page: 页数
    :param page_size: 每页大小
    :return:
    """
    return query.limit(page_size).offset(page_size * (page - 1))


def len_or_none(obj: typing.Any) -> typing.Optional[int]:
    """有数据返回长度 没数据返回None"""
    try:
        return len(obj)
    except TypeError:
        return None


def unwrap_scalars(items: typing.Union[typing.Sequence[Row], Row]) -> typing.Union[
    typing.List[typing.Dict[typing.Text, typing.Any]], typing.Dict[str, typing.Any]]:
    """
    数据库Row对象数据序列化为字典
    :param items: 数据返回数据 [Row(...)]
    :return:
    """
    if isinstance(items, typing.Iterable) and not isinstance(items, Row):
        # 优化列表处理，减少递归
        result = []
        for item in items:
            if isinstance(item, Row):
                # 直接处理Row对象，避免递归
                row_data = dict(zip(item._fields, item._data))
                # 对字典值进行优化处理
                row_result = {}
                for key, value in row_data.items():
                    if isinstance(value, (int, float, str, bool, type(None))):
                        row_result[key] = value
                    else:
                        row_result[key] = default_serialize(value)
                result.append(row_result)
            else:
                result.append(default_serialize(item))
        return result
    elif isinstance(items, Row):
        # 直接处理单个Row对象，避免递归
        row_data = dict(zip(items._fields, items._data))
        # 对字典值进行优化处理
        row_result = {}
        for key, value in row_data.items():
            if isinstance(value, (int, float, str, bool, type(None))):
                row_result[key] = value
            else:
                row_result[key] = default_serialize(value)
        return row_result
    return default_serialize(items)


def default_serialize(obj):
    """默认序列化"""
    try:
        if isinstance(obj, int) and len(str(obj)) > 15:
            return str(obj)
        if isinstance(obj, dict):
            # 优化字典处理，减少递归
            result = {}
            for key, value in obj.items():
                if isinstance(value, (int, float, str, bool, type(None))):
                    result[key] = value
                else:
                    result[key] = default_serialize(value)
            return result
        if isinstance(obj, list):
            # 优化列表处理，减少递归
            result = []
            for i in obj:
                if isinstance(i, (int, float, str, bool, type(None))):
                    result.append(i)
                else:
                    result.append(default_serialize(i))
            return result
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, Row):
            # 直接返回字典，避免递归处理
            data = dict(zip(obj._fields, obj._data))
            # 对字典值进行优化处理
            result = {}
            for key, value in data.items():
                if isinstance(value, (int, float, str, bool, type(None))):
                    result[key] = value
                else:
                    result[key] = default_serialize(value)
            return result
        if hasattr(obj, "__class__") and isinstance(obj.__class__, DeclarativeMeta):
            # 优化ORM对象处理
            result = {}
            for c in obj.__table__.columns:
                value = getattr(obj, c.name)
                if isinstance(value, (int, float, str, bool, type(None))):
                    result[c.name] = value
                else:
                    result[c.name] = default_serialize(value)
            return result
        if isinstance(obj, typing.Callable):
            return repr(obj)
        # 直接使用 jsonable_encoder，避免递归
        return jsonable_encoder(obj)
    except TypeError as err:
        return repr(obj)
