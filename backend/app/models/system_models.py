# -*- coding: utf-8 -*-
# @author: xiaobai
import typing

from sqlalchemy import Column, String, Text, Integer, DateTime, select, update, Index, JSON
from sqlalchemy.orm import aliased

from app.models.base import Base
from app.schemas.system.roles import RoleQuery
from app.schemas.system.user import UserQuery, UserLoginRecordQuery


class User(Base):
    """用户表"""
    __tablename__ = 'user'

    username = Column(String(64), nullable=False, comment='用户名', index=True)
    phone = Column(String(11), nullable=False, comment='手机号', index=True)
    password = Column(Text, nullable=False, comment='密码')
    email = Column(String(64), nullable=True, comment='邮箱')
    status = Column(Integer, nullable=False, comment='用户状态  1 锁定， 0 正常', default=0)
    role_type = Column(Integer, nullable=False, comment='用户类型 10 超级管理员, 20 管理员, 30 普通用户', default=30)
    remarks = Column(String(255), nullable=True, comment='用户描述', default='')
    avatar = Column(Text, nullable=True, comment='头像', default='')
    tags = Column(JSON, nullable=True, comment='标签', default=list)

    @classmethod
    async def get_list(cls, params: UserQuery):
        """
        获取用户列表

        :param params: 查询参数
        :type params: UserQuery
        :return: 分页数据
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        q = [cls.enabled_flag == 1]
        if params.username:
            # 转义LIKE特殊字符 % 和 _，防止通配符注入
            username = params.username.replace('%', '\\%').replace('_', '\\_')
            q.append(cls.username.like(f'%{username}%'))
        if params.user_ids and isinstance(params.user_ids, list):
            q.append(cls.id.in_(params.user_ids))
        # *[getattr(cls, c.name) for c in cls.__table__.columns]
        stmt = select(*cls.get_table_columns()) \
            .where(*q) \
            .order_by(cls.id.desc())
        return await cls.pagination(stmt)

    @classmethod
    async def get_user_by_name(cls, username: str):
        stmt = select(*cls.get_table_columns()).where(cls.username == username, cls.enabled_flag == 1)
        return await cls.get_result(stmt, True)

    @classmethod
    async def get_user_by_phone(cls, phone: str):
        stmt = select(*cls.get_table_columns()).where(cls.phone == phone, cls.enabled_flag == 1)
        return await cls.get_result(stmt, True)


class Menu(Base):
    """菜单表"""
    __tablename__ = 'menu'

    path = Column(String(255), nullable=False, comment='菜单路径')
    name = Column(String(255), nullable=False, comment='菜单名称', index=True)
    component = Column(Integer, nullable=True, comment='组件路径')
    title = Column(String(255), nullable=True, comment='title', index=True)
    isLink = Column(Integer, nullable=True,
                    comment='开启外链条件，`1、isLink: true 2、链接地址不为空（meta.isLink） 3、isIframe: false`')
    isHide = Column(Integer, nullable=True, default=False, comment='菜单是否隐藏（菜单不显示在界面，但可以进行跳转）')
    isKeepAlive = Column(Integer, nullable=True, default=True, comment='菜单是否缓存')
    isAffix = Column(Integer, nullable=True, default=False, comment='固定标签')
    isIframe = Column(Integer, nullable=True, default=False, comment='是否内嵌')
    roles = Column(String(64), nullable=True, default=False, comment='权限')
    icon = Column(String(64), nullable=True, comment='icon', index=True)
    parent_id = Column(Integer, nullable=True, comment='父级菜单id')
    redirect = Column(String(255), nullable=True, comment='重定向路由')
    sort = Column(Integer, nullable=True, comment='排序')
    menu_type = Column(Integer, nullable=True, comment='菜单类型')
    lookup_id = Column(Integer, nullable=True, comment='数据字典')
    active_menu = Column(String(255), nullable=True, comment='显示页签')
    views = Column(Integer, default=0, nullable=True, comment='访问数')

    @classmethod
    async def get_menu_by_ids(cls, ids: typing.List[int]):
        """获取菜单id"""
        stmt = select(cls.get_table_columns()).where(cls.id.in_(ids), cls.enabled_flag == 1).order_by(cls.sort)
        return await cls.get_result(stmt)

    @classmethod
    async def get_menu_all(cls):
        """获取菜单id"""
        stmt = select(cls.get_table_columns()).where(cls.enabled_flag == 1).order_by(cls.sort)
        return await cls.get_result(stmt)

    @classmethod
    async def get_parent_id_by_ids(cls, ids: typing.List[int]):
        """根据子菜单id获取父级菜单id"""
        stmt = select(cls.get_table_columns()).where(cls.id.in_(ids), cls.enabled_flag == 1).order_by(cls.sort)
        return await cls.get_result(stmt)

    @classmethod
    async def get_parent_id_all(cls):
        """根据子菜单id获取父级菜单id"""
        stmt = select(cls.get_table_columns()).where(cls.enabled_flag == 1).order_by(cls.sort)
        return await cls.get_result(stmt)

    @classmethod
    async def get_menu_by_title(cls, title: str):
        stmt = select(cls.get_table_columns()).where(cls.title == title, cls.enabled_flag == 1)
        return await cls.get_result(stmt, True)

    @classmethod
    async def get_menu_by_parent(cls, parent_id: int):
        stmt = select(cls.get_table_columns()) \
            .where(cls.parent_id == parent_id, cls.enabled_flag == 1) \
            .order_by(cls.sort)
        return await cls.get_result(stmt, True)

    @classmethod
    async def add_menu_views(cls, menu_id: int):
        stmt = update(cls.get_table_columns()).where(cls.id == menu_id, cls.enabled_flag == 1).values(
            **{"views": cls.views + 1})
        result = await cls.execute(stmt)
        return result.rowcount


class Roles(Base):
    """角色表"""
    __tablename__ = 'roles'

    name = Column(String(64), nullable=True, comment='菜单名称', index=True)
    role_type = Column(Integer, nullable=False, comment='角色类型 10 超级管理员, 20 管理员, 30 普通用户', index=True, default=30)
    menus = Column(String(500), nullable=True, comment='菜单列表', index=True)
    buttons = Column(Text, nullable=True, comment='按钮权限列表')
    description = Column(String(255), nullable=True, comment='描述')
    status = Column(Integer, nullable=True, comment='状态 1 启用 0 禁用', default=1)

    @classmethod
    async def get_list(cls, params: RoleQuery):
        """
        获取角色列表

        :param params: 查询参数
        :type params: RoleQuery
        :return: 分页数据
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        q = [cls.enabled_flag == 1]
        if params.id:
            q.append(cls.id == params.id)
        if params.name:
            # 转义LIKE特殊字符 % 和 _，防止通配符注入
            name = params.name.replace('%', '\\%').replace('_', '\\_')
            q.append(cls.name.like(f'%{name}%'))
        if params.role_type:
            q.append(cls.role_type == params.role_type)
        else:
            # 默认查询所有角色类型
            pass
        stmt = select(cls.get_table_columns()) \
            .where(*q) \
            .order_by(cls.id.asc())

        return await cls.pagination(stmt)

    @classmethod
    async def get_roles_by_ids(cls, ids: typing.List, role_type=None):
        q = [cls.enabled_flag == 1, cls.id.in_(ids)]
        if role_type:
            q.append(cls.role_type == role_type)
        else:
            # 查询所有角色类型
            pass

        stmt = select(cls.get_table_columns()).where(*q)
        return await cls.get_result(stmt)

    @classmethod
    def get_all(cls, role_type=10):
        q = list()
        if role_type:
            q.append(cls.role_type == role_type)
        return cls.query.filter(*q, cls.enabled_flag == 1).order_by(cls.id.desc())

    @classmethod
    async def get_roles_by_name(cls, name, role_type=None):
        q = [cls.name == name, cls.enabled_flag == 1]
        if role_type:
            q.append(cls.role_type == role_type)
        else:
            # 查询所有角色类型
            pass
        stmt = select(cls.get_table_columns()).where(*q)
        return await cls.get_result(stmt, True)


# Redis 模块级初始化
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config import config as settings
from app.db.redis import RedisPool

# 创建全局 RedisPool 实例
redis_pool = RedisPool()
try:
    redis_pool.init_by_config(settings)
except Exception as e:
    # 初始化失败时记录日志
    import logging
    logging.error(f"Redis 初始化失败: {e}")

class UserLoginRecord(Base):
    __tablename__ = "user_login_record"
    __table_args__ = (
        Index('phone', 'login_time'),
    )

    token = Column(String(40), index=True, comment='登陆token')
    phone = Column(String(64), index=True, comment='手机号')
    user_id = Column(Integer, comment='用户id')
    user_name = Column(String(50), comment='用户名称')
    login_type = Column(String(50), index=True, comment='登陆方式   扫码  账号密码等')
    login_time = Column(DateTime, index=True, comment='登陆时间')
    logout_time = Column(DateTime, comment='退出时间')
    login_ip = Column(String(30), index=True, comment='登录IP')
    ret_msg = Column(String(255), comment='返回信息')
    ret_code = Column(String(9), index=True, comment='是否登陆成功  返回状态码  0成功')

    @classmethod
    async def get_list(cls, params: UserLoginRecordQuery):
        """
        获取用户登录记录列表

        :param params: 查询参数
        :type params: UserLoginRecordQuery
        :return: 分页数据
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        # 开始计时
        import time
        start_time = time.time()
        import json
        import logging
        
        # 尝试从缓存获取
        cache_key = f"login_records:{params.user_id}:{params.page}:{params.page_size}"
        try:
            cached_data = await redis_pool.redis.get(cache_key)
            if cached_data:
                logging.info(f"Redis 缓存命中: {cache_key}")
                logging.info(f"缓存查询耗时: {time.time() - start_time:.4f}s")
                return cached_data
            else:
                logging.info(f"Redis 缓存未命中: {cache_key}")
        except Exception as e:
            # 缓存失败时继续执行数据库查询
            logging.error(f"Redis 缓存获取失败: {e}")
            pass
        
        # 构建查询条件
        q = [cls.enabled_flag == 1]
        if params.user_id:
            q.append(cls.user_id == params.user_id)
        
        # 执行数据库查询
        from sqlalchemy.orm import aliased
        from app.models.system_models import User
        u = aliased(User)
        # 只选择必要的字段，减少数据传输
        stmt = select(
            cls.token,
            cls.phone,
            cls.user_name,
            cls.login_type,
            cls.login_time,
            cls.login_ip,
            cls.ret_msg,
            cls.ret_code,
            cls.enabled_flag,
            cls.trace_id
        ) \
            .where(*q) \
            .order_by(cls.id.desc())
        
        query_start_time = time.time()
        result = await cls.pagination(stmt)
        query_end_time = time.time()
        logging.info(f"数据库查询耗时: {query_end_time - query_start_time:.4f}s")
        
        # 缓存结果，过期时间1小时
        try:
            await redis_pool.redis.set(cache_key, json.dumps(result), ex=3600)
            logging.info(f"Redis 缓存设置成功: {cache_key}")
        except Exception as e:
            # 缓存失败时忽略，继续返回结果
            logging.error(f"Redis 缓存设置失败: {e}")
            pass
        
        # 结束计时
        end_time = time.time()
        logging.info(f"总执行耗时: {end_time - start_time:.4f}s")
        return result

    @classmethod
    async def get_by_token(cls, token: str):
        if not token:
            return None
        stmt = select(cls.get_table_columns()).where(cls.enabled_flag == 1, cls.token == token).order_by(cls.id.desc())
        return await cls.get_result(stmt, first=True)


class FileInfo(Base):
    """文件信息"""
    __tablename__ = 'file_info'
    id = Column(String(60), nullable=False, primary_key=True, autoincrement=False)
    name = Column(String(255), nullable=True, comment='存储的文件名')
    file_path = Column(String(255), nullable=True, comment='文件路径')
    extend_name = Column(String(255), nullable=True, comment='扩展名称', index=True)
    original_name = Column(String(255), nullable=True, comment='原名称')
    content_type = Column(String(255), nullable=True, comment='文件类型')
    file_size = Column(String(255), nullable=True, comment='文件大小')
