import typing

from loguru import logger
from pydantic import BaseModel, Field, model_validator

from app.schemas.base import BaseSchema


class RoleIn(BaseModel):
    id: typing.Optional[int] = Field(None, description="角色id")
    name: str = Field(..., description="角色名称")
    role_type: int = Field(default=30, description="角色类型 10 超级管理员, 20 管理员, 30 普通用户")
    menus: str = Field(..., description="菜单列表")
    buttons: typing.Optional[str] = Field(None, description="按钮权限列表")
    description: typing.Optional[str] = Field(None, description="描述")
    status: typing.Optional[int] = Field(default=1, description="状态 1 启用 0 禁用")

    @model_validator(mode="before")
    def root_validator(cls, data: typing.Dict[typing.Text, typing.Any]):
        """
        数据验证器
        
        处理菜单和按钮权限数据的格式转换
        
        :param data: 输入数据
        :type data: typing.Dict[typing.Text, typing.Any]
        :return: 处理后的数据
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        logger.info(f"验证器接收到的原始数据: {data}")
        
        menus = data.get("menus", [])
        logger.info(f"menus原始值: {menus}, 类型: {type(menus)}")
        
        if menus:
            # 如果menus是列表，转换为逗号分隔的字符串
            if isinstance(menus, list):
                data["menus"] = ','.join(list(map(str, menus)))
                logger.info(f"menus列表转换为字符串: {data['menus']}")
            # 如果menus已经是字符串，直接使用
            elif isinstance(menus, str):
                data["menus"] = menus
                logger.info(f"menus已经是字符串: {data['menus']}")
        
        buttons = data.get("buttons", [])
        logger.info(f"buttons原始值: {buttons}, 类型: {type(buttons)}")
        
        if buttons:
            # 如果buttons是列表，转换为逗号分隔的字符串
            if isinstance(buttons, list):
                data["buttons"] = ','.join(list(map(str, buttons)))
                logger.info(f"buttons列表转换为字符串: {data['buttons']}")
            # 如果buttons已经是字符串，直接使用
            elif isinstance(buttons, str):
                data["buttons"] = buttons
                logger.info(f"buttons已经是字符串: {data['buttons']}")
        
        logger.info(f"验证器处理后的数据: {data}")
        return data


class RoleQuery(BaseSchema):
    id: typing.Optional[int] = Field(None, description="角色id")
    name: typing.Optional[str] = Field(None, description="角色名称")
    role_type: typing.Optional[int] = Field(None, description="角色类型 10 超级管理员, 20 管理员, 30 普通用户")


class RoleDel(BaseModel):
    id: int = Field(..., description="角色id")
