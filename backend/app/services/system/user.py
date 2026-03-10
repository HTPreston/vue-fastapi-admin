import asyncio
import traceback
import typing
import uuid
from datetime import datetime

from loguru import logger

from app.corelibs import g
from app.corelibs.codes import CodeEnum
from app.corelibs.consts import TEST_USER_INFO, CACHE_DAY
from app.db import redis_pool
from app.models.system_models import User, Menu,  UserLoginRecord
from app.schemas.system.user import (UserLogin, UserIn, UserResetPwd, UserDel,
                                     UserQuery,UserLoginRecordIn, UserProfileUpdate,
                                     UserAvatarUpdate, UserEmailUpdate, UserPhoneUpdate, UserRegister)
from app.services.system.menu import MenuService
from app.utils.context import FastApiRequest
from app.utils.current_user import current_user
from app.utils.des import encrypt_rsa_password, decrypt_rsa_password
from app.utils.serialize import default_serialize


class UserService:
    """用户类"""

    @staticmethod
    async def login(params: UserLogin) -> typing.Dict[typing.Text, typing.Any]:
        """
        登录
        :return:
        """
        username = params.username
        phone = params.phone
        password = params.password
        
        if not password:
            raise ValueError(CodeEnum.PARTNER_CODE_PARAMS_FAIL.msg)
        
        # 支持手机号或用户名登录
        user_info = None
        if phone:
            # 优先使用手机号登录
            user_info = await User.get_user_by_phone(phone)
        elif username:
            # 使用用户名登录
            user_info = await User.get_user_by_name(username)
        
        if not user_info:
            raise ValueError(CodeEnum.WRONG_USER_NAME_OR_PASSWORD.msg)
        u_password = decrypt_rsa_password(user_info["password"])

        if u_password != password:
            raise ValueError(CodeEnum.WRONG_USER_NAME_OR_PASSWORD.msg)
        token = str(uuid.uuid4())
        login_time = default_serialize(datetime.now())
        tags = user_info.get("tags", None)

        token_user_info = {
            "id": user_info["id"],
            "token": token,
            "login_time": login_time,
            "username": user_info["username"],
            "phone": user_info.get("phone", ""),
            "tags": tags if tags else [],
            "role_type": user_info.get("role_type")
        }
        await redis_pool.redis.set(TEST_USER_INFO.format(token), token_user_info, CACHE_DAY)
        logger.info('用户 [{}] 登录了系统'.format(user_info["username"]))

        asyncio.create_task(UserService.login_record("login", token_user_info, token))
        return token_user_info

    @staticmethod
    async def logout():
        """
        登出
        :return:
        """
        token = FastApiRequest.get().headers.get('token', None)
        try:
            token_user_info = await current_user(token)
            await redis_pool.redis.delete(TEST_USER_INFO.format(token))
            asyncio.create_task(UserService.login_record("logout", token_user_info, token))
        except Exception as err:
            logger.error(traceback.format_exc())

    @staticmethod
    async def login_record(record_type: str, user_token_info: dict, token: str):
        try:
            if record_type == 'login':
                login_ip = FastApiRequest.get().headers.get("X-Real-IP", None)
                if not login_ip:
                    login_ip = FastApiRequest.get().client.host
                params = UserLoginRecordIn(
                    token=token,
                    phone=user_token_info.get("phone", ""),
                    user_id=user_token_info["id"],
                    user_name=user_token_info["username"],
                    logout_type=None,
                    login_type="账号密码",
                    login_time=user_token_info['login_time'],
                    logout_time=None,
                    login_ip=login_ip,
                    ret_code="0",
                    ret_msg="登录成功",
                    address="未知地址",
                    source_type="系统登录"
                )
                await UserLoginRecord.create_or_update(params.dict())
            elif record_type == 'logout':
                login_recode = await UserLoginRecord.get_by_token(token)
                if login_recode:
                    await UserLoginRecord.update({"id": login_recode['id'], "logout_time": datetime.now()})

        except Exception as exc:
            logger.error(f"登录日志记录错误\n{traceback.format_exc(3)}")

    @staticmethod
    async def user_register(user_params: UserRegister) -> typing.Dict[typing.Text, typing.Any]:
        """
        用户注册

        :param user_params: 用户注册参数
        :type user_params: UserRegister
        :return: 用户信息包含token
        :rtype: typing.Dict[typing.Text, typing.Any]
        :raises ValueError: 手机号已注册
        """
        # 检查手机号是否已存在
        phone_user = await User.get_user_by_phone(user_params.phone)
        if phone_user:
            raise ValueError("手机号已被注册")

        # 设置默认值
        user_data = user_params.dict()
        user_data['role_type'] = 30  # 默认普通用户
        user_data['status'] = 1  # 默认正常状态
        user_data['avatar'] = 'https://api.dicebear.com/7.x/avataaars/svg?seed=' + user_params.username  # 默认头像

        # 加密密码
        if user_data.get('password'):
            user_data['password'] = encrypt_rsa_password(user_data['password'])

        # 创建用户并获取用户数据（字典形式，避免查询导致的序列化问题）
        user = await User.create(user_data, to_dict=True)

        # 生成 token 并保存到 redis（自动登录）
        token = str(uuid.uuid4())
        login_time = default_serialize(datetime.now())

        # 处理 tags 字段，确保是列表
        tags = user.get('tags', [])
        if callable(tags):
            tags = []
        elif not isinstance(tags, list):
            tags = []

        token_user_info = {
            "id": user.get('id'),
            "token": token,
            "login_time": login_time,
            "username": user.get('username'),
            "phone": user.get('phone'),
            "tags": tags,
            "avatar": user.get('avatar'),
            "role_type": user.get('role_type')
        }
        await redis_pool.redis.set(TEST_USER_INFO.format(token), token_user_info, CACHE_DAY)
        logger.info(f"用户 [{user.get('username')}] 注册并自动登录")

        return token_user_info

    @staticmethod
    async def list(params: UserQuery) -> typing.Dict[typing.Text, typing.Any]:
        """
        获取用户列表
        :param params:  查询参数
        :return:
        """
        data = await User.get_list(params)
        for row in data.get("rows"):
            tags = row.get("tags", None)
            row["tags"] = tags if tags else []
        return data

    @staticmethod
    async def save_or_update(params: UserIn) -> typing.Dict[typing.Text, typing.Any]:
        """
        用户保存方法
        :param params: 用户字段
        :return:
        """
        result = await User.create_or_update(params.dict())
        current_user_info = await current_user()
        if current_user_info.get("id") == params.id:
            token_user_info = {
                "id": result["id"],
                "token": current_user_info.get("token"),
                "login_time": current_user_info.get("login_time"),
                "username": result["username"],
                "phone": result.get("phone", ""),
                "tags": result["tags"],
                "role_type": result.get("role_type")
            }
            await redis_pool.redis.set(TEST_USER_INFO.format(g.token), token_user_info, CACHE_DAY)
        return result

    @staticmethod
    async def get_login_records(page: int = 1, page_size: int = 10) -> typing.Dict[typing.Text, typing.Any]:
        """
        获取当前用户的登录记录

        :param page: 页码
        :type page: int
        :param page_size: 每页数量
        :type page_size: int
        :return: 登录记录列表
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        current_user_info = await current_user()
        if not current_user_info:
            raise ValueError(CodeEnum.PARTNER_CODE_TOKEN_EXPIRED_FAIL.msg)
        
        user_id = current_user_info.get("id")
        
        # 构建查询参数
        from app.schemas.system.user import UserLoginRecordQuery
        params = UserLoginRecordQuery(
            page=page,
            page_size=page_size,
            user_id=user_id
        )
        
        result = await UserLoginRecord.get_list(params)
        return result

    @staticmethod
    async def deleted(params: UserDel):
        """
        删除用户
        :param params: 删除参数
        :return:
        """
        try:
            return await User.delete(params.id)
        except Exception as err:
            logger.error(traceback.format_exc())

    @staticmethod
    async def check_token(token: str) -> typing.Dict[typing.Text, typing.Any]:
        """
        校验token
        :param token: token
        :return:
        """
        user_info = await redis_pool.redis.get(TEST_USER_INFO.format(token))
        if not user_info:
            raise ValueError(CodeEnum.PARTNER_CODE_TOKEN_EXPIRED_FAIL.msg)

        user_info = {
            'id': user_info.get('id', None),
            'username': user_info.get('username', None)
        }
        return user_info

    @staticmethod
    async def reset_password(params: UserResetPwd):
        """修改密码"""

        if params.new_pwd != params.re_new_pwd:
            raise ValueError(CodeEnum.PASSWORD_TWICE_IS_NOT_AGREEMENT.msg)
        user_info = await User.get(params.id)
        pwd = decrypt_rsa_password(user_info.password)
        if params.old_pwd != pwd:
            raise ValueError(CodeEnum.OLD_PASSWORD_ERROR.msg)
        if params.new_pwd == pwd:
            raise ValueError(CodeEnum.NEW_PWD_NO_OLD_PWD_EQUAL.msg)
        new_pwd = encrypt_rsa_password(params.new_pwd)
        await User.update({"password": new_pwd, "id": params.id})

    @staticmethod
    async def get_user_info_by_token() -> typing.Union[typing.Dict[typing.Text, typing.Any], None]:
        """根据token获取用户信息"""
        token_user_info = await current_user()
        if not token_user_info or not isinstance(token_user_info, dict):
            raise ValueError(CodeEnum.PARTNER_CODE_TOKEN_EXPIRED_FAIL.value[1])
        user_id = token_user_info.get("id")
        if not user_id:
            raise ValueError(CodeEnum.PARTNER_CODE_TOKEN_EXPIRED_FAIL.value[1])
        user_info = await User.get(user_id)
        if not user_info:
            raise ValueError(CodeEnum.PARTNER_CODE_TOKEN_EXPIRED_FAIL.value[1])
        
        # 获取用户的按钮权限
        button_permissions = []
        if hasattr(user_info, 'role_type') and user_info.role_type:
            # 根据用户类型查询对应的角色
            from app.models.system_models import Roles
            from sqlalchemy import select
            
            # 构建查询语句
            stmt = select(Roles.get_table_columns()).where(
                Roles.role_type == user_info.role_type,
                Roles.enabled_flag == 1
            )
            
            # 执行查询
            roles = await Roles.get_result(stmt)
            
            # 提取按钮权限
            for role in roles:
                if role.get('buttons'):
                    button_permissions.extend(role['buttons'].split(','))
            
            # 去重
            button_permissions = list(set(button_permissions))
        
        return {
            "id": user_info.id,
            "avatar": user_info.avatar,
            "username": user_info.username,
            "phone": user_info.phone,
            "email": user_info.email,
            "remarks": user_info.remarks,
            "tags": user_info.tags,
            "role_type": user_info.role_type,
            "login_time": token_user_info.get("login_time", None),
            "buttons": button_permissions
        }

    @staticmethod
    async def get_menu_by_token() -> typing.List[typing.Dict[typing.Text, typing.Any]]:
        """
        菜单权限
        
        根据用户角色获取对应的菜单权限列表
        
        :return: 菜单权限列表
        :rtype: typing.List[typing.Dict[typing.Text, typing.Any]]
        """
        current_user_info = await current_user()
        if not current_user_info:
            return []
        user_info = await User.get(current_user_info.get("id"))
        if not user_info:
            return []
        
        menu_ids = []
        # 根据用户类型查询对应的角色
        if hasattr(user_info, 'role_type') and user_info.role_type:
            from app.models.system_models import Roles
            from sqlalchemy import select
            
            # 构建查询语句
            stmt = select(Roles.get_table_columns()).where(
                Roles.role_type == user_info.role_type,
                Roles.enabled_flag == 1
            )
            
            # 执行查询
            role_list = await Roles.get_result(stmt)
            
            # 提取菜单 ID
            for i in role_list:
                if i.get("menus"):
                    menu_ids += list(map(int, i["menus"].split(',')))
        
        if not menu_ids:
            return []
        
        parent_menus = await Menu.get_parent_id_by_ids(list(set(menu_ids)))
        # 前端角色报错只保存子节点数据，所有这里要做处理，把父级菜单也返回给前端
        menu_ids += [i["parent_id"] for i in parent_menus]
        all_menu = await Menu.get_menu_by_ids(list(set(menu_ids)))
        parent_menu = [menu for menu in all_menu if menu['parent_id'] == 0]
        return MenuService.menu_assembly(parent_menu, all_menu) if menu_ids else []

    @staticmethod
    async def update_profile(params: UserProfileUpdate) -> typing.Dict[typing.Text, typing.Any]:
        """
        更新个人信息

        :param params: 个人信息参数
        :type params: UserProfileUpdate
        :return: 更新后的用户信息
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        current_user_info = await current_user()
        if not current_user_info:
            raise ValueError(CodeEnum.PARTNER_CODE_TOKEN_EXPIRED_FAIL.msg)
        
        user_id = current_user_info.get("id")
        update_data = {}

        if params.username:
            update_data["username"] = params.username

        if params.email:
            update_data["email"] = params.email
        
        if params.avatar:
            update_data["avatar"] = params.avatar
        
        if params.remarks:
            update_data["remarks"] = params.remarks
        
        if params.tags is not None:
            update_data["tags"] = params.tags
        
        if not update_data:
            raise ValueError('没有需要更新的信息')
        
        update_data["id"] = user_id
        result = await User.create_or_update(update_data)
        
        # 更新 Redis 中的用户信息
        token_user_info = {
            "id": result["id"],
            "token": current_user_info.get("token"),
            "login_time": current_user_info.get("login_time"),
            "username": result["username"],
            "phone": result.get("phone", ""),
            "tags": result["tags"],
            "role_type": result.get("role_type")
        }
        await redis_pool.redis.set(TEST_USER_INFO.format(g.token), token_user_info, CACHE_DAY)

        return result

    @staticmethod
    async def update_avatar(params: UserAvatarUpdate) -> typing.Dict[typing.Text, typing.Any]:
        """
        更新用户头像

        :param params: 头像参数
        :type params: UserAvatarUpdate
        :return: 更新后的用户信息
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        current_user_info = await current_user()
        if not current_user_info:
            raise ValueError(CodeEnum.PARTNER_CODE_TOKEN_EXPIRED_FAIL.msg)
        
        user_id = current_user_info.get("id")
        result = await User.create_or_update({"id": user_id, "avatar": params.avatar})
        
        # 更新 Redis 中的用户信息
        token_user_info = {
            "id": result["id"],
            "token": current_user_info.get("token"),
            "login_time": current_user_info.get("login_time"),
            "username": result["username"],
            "tags": result["tags"],
            "role_type": result.get("role_type")
        }
        await redis_pool.redis.set(TEST_USER_INFO.format(g.token), token_user_info, CACHE_DAY)

        return result

    @staticmethod
    async def update_email(params: UserEmailUpdate) -> typing.Dict[typing.Text, typing.Any]:
        """
        更新用户邮箱

        :param params: 邮箱参数
        :type params: UserEmailUpdate
        :return: 更新后的用户信息
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        current_user_info = await current_user()
        if not current_user_info:
            raise ValueError(CodeEnum.PARTNER_CODE_TOKEN_EXPIRED_FAIL.msg)
        
        user_id = current_user_info.get("id")
        result = await User.create_or_update({"id": user_id, "email": params.email})
        
        return result

    @staticmethod
    async def update_phone(params: UserPhoneUpdate) -> typing.Dict[typing.Text, typing.Any]:
        """
        更新用户手机号

        :param params: 手机号参数
        :type params: UserPhoneUpdate
        :return: 更新后的用户信息
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        current_user_info = await current_user()
        if not current_user_info:
            raise ValueError(CodeEnum.PARTNER_CODE_TOKEN_EXPIRED_FAIL.msg)
        
        user_id = current_user_info.get("id")
        result = await User.create_or_update({"id": user_id, "phone": params.phone})
        
        return result

