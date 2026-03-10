# -*- coding: utf-8 -*-
# @author: xiaobai
"""
个人中心模块 (Identity Center)

提供个人中心相关功能，包括：
- 获取个人信息
- 更新个人信息
- 更新头像
- 更新手机号
- 更新邮箱
- 修改密码
- 获取个人菜单权限
"""
from app.corelibs.custom_router import APIRouter
from app.schemas.system.user import (
    UserResetPwd,
    UserProfileUpdate,
    UserAvatarUpdate,
    UserEmailUpdate,
    UserPhoneUpdate
)
from app.services.system.user import UserService
from app.utils.response import HttpResponse

router = APIRouter()


@router.post('/getUserInfo', description="获取个人信息")
async def get_user_info():
    """
    获取当前登录用户的个人信息
    
    :return: 用户详细信息
    """
    user_info = await UserService.get_user_info_by_token()
    return await HttpResponse.success(user_info)


@router.post('/updateProfile', description="更新个人信息")
async def update_profile(params: UserProfileUpdate):
    """
    更新个人信息
    
    支持更新：昵称、邮箱、头像、个人描述
    
    :param params: 个人信息参数
    :return: 更新后的用户信息
    """
    result = await UserService.update_profile(params)
    return await HttpResponse.success(result)


@router.post('/updateAvatar', description="更新头像")
async def update_avatar(params: UserAvatarUpdate):
    """
    更新用户头像
    
    :param params: 头像参数
    :return: 更新后的用户信息
    """
    result = await UserService.update_avatar(params)
    return await HttpResponse.success(result)


@router.post('/updateEmail', description="更新邮箱")
async def update_email(params: UserEmailUpdate):
    """
    更新用户邮箱
    
    :param params: 邮箱参数
    :return: 更新后的用户信息
    """
    result = await UserService.update_email(params)
    return await HttpResponse.success(result)


@router.post('/updatePhone', description="更新手机号")
async def update_phone(params: UserPhoneUpdate):
    """
    更新用户手机号
    
    :param params: 手机号参数
    :return: 更新后的用户信息
    """
    result = await UserService.update_phone(params)
    return await HttpResponse.success(result)


@router.post('/resetPassword', description="修改密码")
async def reset_password(params: UserResetPwd):
    """
    修改个人密码

    :param params: 密码参数
    :return: 修改结果
    """
    await UserService.reset_password(params)
    return await HttpResponse.success()


@router.post('/getLoginRecords', description="获取登录记录")
async def get_login_records(page: int = 1, page_size: int = 10):
    """
    获取当前用户的登录记录

    :param page: 页码，默认为1
    :type page: int
    :param page_size: 每页数量，默认为10
    :type page_size: int
    :return: 登录记录列表
    """
    result = await UserService.get_login_records(page, page_size)
    return await HttpResponse.success(result)


@router.post('/getMenu', description="获取个人菜单权限")
async def get_menu():
    """
    获取当前用户的菜单权限
    
    :return: 菜单列表
    """
    user_info = await UserService.get_menu_by_token()
    return await HttpResponse.success(user_info)
