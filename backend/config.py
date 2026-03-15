# -*- coding: utf-8 -*-
# @author: xiaobai
import os
import typing

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

project_desc = """
    🎉 fast-element-admin 管理员接口汇总 🎉
    ✨ 账号: admin ✨
    ✨ 密码: 123456 ✨
    ✨ 权限(scopes): admin ✨
"""


class Configs(BaseSettings):
    SERVER_DESC: str = project_desc  # 描述
    SERVER_VERSION: typing.Union[int, str] = 2.0  # 版本
    BASE_URL: AnyHttpUrl = "http://127.0.0.1:8100"  # 开发环境

    API_PREFIX: str = "/api"  # 接口前缀
    STATIC_DIR: str = 'static'  # 静态文件目录
    GLOBAL_ENCODING: str = 'utf8'  # 全局编码
    CORS_ORIGINS: typing.List[typing.Any] = ["*"]  # 跨域请求
    WHITE_ROUTER: typing.List[str] = ["/api/user/login", "/api/user/userRegister"]  # 路由白名单，不需要鉴权

    SECRET_KEY: str = "kPBDjVk0o3Y1wLxdODxBpjwEjo7-Euegg4kdnzFIRjc"  # 密钥(每次重启服务密钥都会改变, token解密失败导致过期, 可设置为常量)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1  # token过期时间: 60 minutes * 24 hours * 1 days = 1 days

    # redis
    REDIS_URI: str = Field(..., validation_alias="REDIS_URI")  # redis

    # DATABASE_URI: str = "sqlite+aiosqlite:///./sql_app.db?check_same_thread=False"  # Sqlite(异步)
    DATABASE_URI: str = Field(..., validation_alias="MYSQL_DATABASE_URI")  # MySQL(异步)
    # DATABASE_URI: str = "postgresql+asyncpg://postgres:123456@localhost:5432/postgres"  # PostgreSQL(异步)
    DATABASE_ECHO: bool = False  # 是否打印数据库日志 (可看到创建表、表数据增删改查的信息)

    # logger
    LOGGER_DIR: str = "logs"  # 日志文件夹名
    LOGGER_NAME: str = 'HTHC.log'  # 日志文件名  (时间格式 {time:YYYY-MM-DD_HH-mm-ss}.log)
    LOGGER_LEVEL: str = 'INFO'  # 日志等级: ['DEBUG' | 'INFO']
    LOGGER_ROTATION: str = "10 MB"  # 日志分片: 按 时间段/文件大小 切分日志. 例如 ["500 MB" | "12:00" | "1 week"]
    LOGGER_RETENTION: str = "7 days"  # 日志保留的时间: 超出将删除最早的日志. 例如 ["1 days"]

    # dir
    BASEDIR: str = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

    TEST_FILES_DIR: str = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'files')

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env", env_file_encoding="utf-8", extra="ignore")


config = Configs()
