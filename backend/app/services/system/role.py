import traceback
import typing

from loguru import logger

from app.models.system_models import Roles, User
from app.schemas.system.roles import RoleQuery, RoleIn, RoleDel
from app.utils.current_user import current_user


class RolesService:
    """角色类"""

    @staticmethod
    async def list(params: RoleQuery) -> typing.Dict[str, typing.Any]:
        data = await Roles.get_list(params)
        for row in data.get("list", []):
            row["menus"] = list(map(int, (row["menus"].split(",")))) if row["menus"] else []
            row["buttons"] = row["buttons"].split(",") if row["buttons"] else []
        return data

    @staticmethod
    async def save_or_update(params: RoleIn) -> int:
        logger.info(f"服务层接收到的参数: {params}")
        logger.info(f"params.dict(): {params.dict()}")
        
        # 获取当前登录用户信息
        current_user_info = await current_user()
        current_role_type = current_user_info.get('role_type') if current_user_info else None
        
        # 检查权限：如果要新增或编辑权限类型为10的角色，只有超级管理员(role_type=10)才能操作
        if params.role_type == 10 and current_role_type != 10:
            raise ValueError('无权限操作：只有超级管理员才能创建或编辑超级管理员角色!')
        
        # 检查权限：无法新增高等级权限角色（权限等级：10 > 20 > 30）
        if not params.id:  # 只有新增时需要检查
            if current_role_type and params.role_type < current_role_type:
                raise ValueError(f'无权限操作：无法创建更高权限的角色!')
        
        if params.id:
            role_info = await Roles.get(params.id)
            # 检查是否在编辑超级管理员角色
            if role_info and role_info.role_type == 10 and current_role_type != 10:
                raise ValueError('无权限操作：只有超级管理员才能编辑超级管理员角色!')
            
            # 检查是否在编辑更高权限的角色
            if role_info and role_info.role_type < current_role_type:
                raise ValueError('无权限操作：无法编辑更高权限的角色!')
            
            if role_info.name != params.name:
                if await Roles.get_roles_by_name(params.name):
                    raise ValueError('角色名已存在!')
        else:
            if await Roles.get_roles_by_name(params.name):
                raise ValueError('角色名已存在!')
        result = await Roles.create_or_update(params.dict())
        logger.info(f"保存后的结果: {result}")
        return result

    @staticmethod
    async def deleted(params: RoleDel) -> int:
        try:
            # 检查角色是否为超级管理员角色
            role_info = await Roles.get(params.id, to_dict=True)
            if role_info and role_info.get('role_type') == 10:
                raise ValueError('超级管理员角色不可删除!')
            
            relation_data = await User.get_user_by_roles(params.id)
            # if relation_data:
            #     raise ValueError('有用户关联了当前角色，不允许删除!')
            # return await Roles.delete(params.id)
        except Exception as err:
            logger.error(traceback.format_exc())
            raise
