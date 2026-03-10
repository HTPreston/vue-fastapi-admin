# -*- coding: utf-8 -*-
# @author: xiaobai
import typing

from pydantic import BaseModel, Field
from app.schemas.base import BaseSchema
from app.utils.des import decrypt_rsa_password


class UserIn(BaseModel):
    id: typing.Optional[int] = Field(None, title="id", description='用户id')
    username: typing.Optional[str] = Field(..., title="用户名不能为空！", description='用户名')
    phone: typing.Optional[str] = Field(..., title="手机号不能为空！", description='手机号')
    email: typing.Optional[str] = Field(None, description='邮箱')
    role_type: typing.Optional[int] = Field(None, description='用户类型 10 超级管理员 20 管理员 30 普通用户')
    status: typing.Optional[int] = Field(None, description='用户状态 1 正常 0 锁定')
    remarks: typing.Optional[str] = Field(None, description='用户描述')
    avatar: typing.Optional[str] = Field(None, description='头像')
    tags: typing.Optional[typing.List] = Field(None, description='用户标签')
    password: typing.Optional[str] = Field(description='密码', default=decrypt_rsa_password("123456"))


class UserUpdate(BaseModel):
    id: typing.Optional[int] = Field(..., title="id", description='用户id')
    username: typing.Optional[str] = Field(None, description='用户名')
    phone: typing.Optional[str] = Field(None, description='手机号')
    email: typing.Optional[str] = Field(None, description='邮箱')
    role_type: typing.Optional[int] = Field(None, description='用户类型 10 超级管理员 20 管理员 30 普通用户')
    status: typing.Optional[int] = Field(None, description='用户状态 1 正常 0 锁定')
    remarks: typing.Optional[str] = Field(None, description='用户描述')
    avatar: typing.Optional[str] = Field(None, description='头像')
    tags: typing.Optional[typing.List] = Field(None, description='用户标签')
    password: typing.Optional[str] = Field(None, description='密码')


class UserRegister(BaseModel):
    """用户注册"""
    username: typing.Optional[str] = Field(..., title="用户名不能为空！", description='用户名')
    phone: typing.Optional[str] = Field(..., title="手机号不能为空！", description='手机号')
    password: typing.Optional[str] = Field(..., title="密码不能为空！", description='密码')


class UserDel(BaseModel):
    id: int = Field(..., title="id", description='id')


class UserQuery(BaseSchema):
    username: typing.Optional[str] = Field(None, description='用户名')
    user_ids: typing.Optional[typing.List[int]] = Field(None, description='用户id列表')


class UserLogin(BaseModel):
    username: typing.Optional[str] = Field(None, description='用户名')
    phone: typing.Optional[str] = Field(None, description='手机号')
    password: typing.Optional[str] = Field(..., description='密码')


class UserResetPwd(BaseModel):
    id: int = Field(..., description='用户id')
    old_pwd: typing.Optional[str] = Field(..., description='旧密码')
    new_pwd: typing.Optional[str] = Field(..., description='新密码')
    re_new_pwd: typing.Optional[str] = Field(..., description='二次输入新密码')


class UserLoginRecordIn(BaseModel):
    token: typing.Optional[str] = Field(None, description='token')
    phone: typing.Optional[str] = Field(None, description="手机号")
    user_id: typing.Optional[int] = Field(None, description="用户id")
    user_name: typing.Optional[str] = Field(None, description="用户名称")
    login_type: typing.Optional[str] = Field(None, description="登录类型")
    login_time: typing.Optional[str] = Field(None, description="登录时间")
    logout_time: typing.Optional[str] = Field(None, description="登出时间")
    login_ip: typing.Optional[str] = Field(None, description="登录ip")
    ret_msg: typing.Optional[str] = Field(None, description="返回信息")
    ret_code: typing.Optional[str] = Field(None, description="返回code")


class UserLoginRecordQuery(BaseModel):
    page: typing.Optional[int] = Field(1, description='页码')
    page_size: typing.Optional[int] = Field(10, description='每页数量')
    token: typing.Optional[str] = Field(None, description='token')
    phone: typing.Optional[str] = Field(None, description="手机号")
    user_id: typing.Optional[int] = Field(None, description="用户id")
    user_name: typing.Optional[str] = Field(None, description="用户名称")
    login_type: typing.Optional[str] = Field(None, description="登录类型")
    login_time: typing.Optional[str] = Field(None, description="登录时间")
    logout_time: typing.Optional[str] = Field(None, description="登出时间")
    login_ip: typing.Optional[str] = Field(None, description="登录ip")
    ret_msg: typing.Optional[str] = Field(None, description="返回信息")
    ret_code: typing.Optional[str] = Field(None, description="返回code")


class UserProfileUpdate(BaseModel):
    """个人信息更新"""
    username: typing.Optional[str] = Field(None, description='用户名')
    email: typing.Optional[str] = Field(None, description='邮箱')
    avatar: typing.Optional[str] = Field(None, description='头像')
    remarks: typing.Optional[str] = Field(None, description='用户描述')
    tags: typing.Optional[typing.List] = Field(None, description='用户标签')


class UserAvatarUpdate(BaseModel):
    """头像更新"""
    avatar: typing.Optional[str] = Field(..., description='头像地址')


class UserEmailUpdate(BaseModel):
    """邮箱更新"""
    email: typing.Optional[str] = Field(..., description='邮箱')


class UserPhoneUpdate(BaseModel):
    """手机号更新"""
    phone: typing.Optional[str] = Field(..., description='手机号')
