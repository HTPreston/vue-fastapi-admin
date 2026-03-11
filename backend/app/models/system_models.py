import typing

from sqlalchemy import Column, String, Text, Integer, DateTime, select, update, Index, JSON
from sqlalchemy import SmallInteger, Date, TIMESTAMP, Numeric

from datetime import datetime

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


class CompanyInfo(Base):
    """公司信息"""
    __tablename__ = 'company_info'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False, comment='公司名称')
    short_name = Column(String(200), nullable=True, comment='公司简称')
    english_name = Column(String(200), nullable=True, comment='英文名称')
    credit_code = Column(String(50), nullable=True, comment='统一社会信用代码')
    legal_representative = Column(String(100), nullable=True, comment='法人代表人')
    registered_capital = Column(Integer, nullable=True, comment='注册资本')
    establishment_date = Column(Date, nullable=True, comment='成立日期')
    business_term = Column(String(100), nullable=True, comment='经营期限')
    company_type = Column(String(50), nullable=True, comment='企业类型')
    business_scope = Column(Text, nullable=True, comment='经营范围')
    registered_address = Column(String(500), nullable=True, comment='注册地址')
    office_address = Column(String(500), nullable=True, comment='办公地址')
    postal_code = Column(String(20), nullable=True, comment='邮政编码')
    contact_phone = Column(String(20), nullable=True, comment='联系电话')
    fax = Column(String(50), nullable=True, comment='传真号码')
    website = Column(String(200), nullable=True, comment='公司网址')
    email = Column(String(100), nullable=True, comment='电子邮箱')
    personnel_reserve = Column(JSON, nullable=True, comment='人员储备')
    bank_name = Column(String(100), nullable=True, comment='开户银行')
    bank_account = Column(String(100), nullable=True, comment='银行账号')
    business_license_path = Column(String(500), nullable=True, comment='营业执照图片路径')
    deposit_account_path = Column(String(500), nullable=True, comment='存款账户图片路径')
    status = Column(SmallInteger, nullable=False, default=1, comment='状态:1-正常,0-停用')
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now, comment='创建时间')
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    @classmethod
    async def get_list(cls, params: typing.Dict) -> typing.Dict[typing.Text, typing.Any]:
        """
        获取公司信息列表

        :param params: 查询参数
        :type params: typing.Dict
        :return: 分页数据
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        q = [cls.enabled_flag == 1]
        if params.get('name'):
            name = params['name'].replace('%', '\\%').replace('_', '\\_')
            q.append(cls.name.like(f'%{name}%'))
        if params.get('status') is not None:
            q.append(cls.status == params['status'])

        return await cls.get_list_by_page(q, params.get('page', 1), params.get('page_size', 10))


class CompanyQualificationCertificate(Base):
    """公司资质证书表"""
    __tablename__ = 'company_qualification_certificate'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True, comment='主键ID')
    company_id = Column(Integer, nullable=False, comment='公司ID')
    certificate_type = Column(String(50), nullable=False, comment='资质类型')
    certificate_level = Column(String(500), nullable=True, comment='资质等级')
    certificate_no = Column(String(100), nullable=True, comment='证书编号')
    certificate_name = Column(String(200), nullable=True, comment='证书全称')
    issue_authority = Column(String(200), nullable=True, comment='发证机关')
    issue_date = Column(Date, nullable=True, comment='发证日期')
    valid_until = Column(Date, nullable=True, comment='有效期至')
    certificate_status = Column(SmallInteger, nullable=True, default=1, comment='证书状态:1-有效,0-无效,2-即将到期')
    certificate_path = Column(String(500), nullable=True, comment='证书图片路径')
    remark = Column(Text, nullable=True, comment='备注')
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now, comment='创建时间')
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    @classmethod
    async def get_list(cls, params: typing.Dict) -> typing.Dict[typing.Text, typing.Any]:
        """
        获取公司资质证书列表

        :param params: 查询参数
        :type params: typing.Dict
        :return: 分页数据
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        q = [cls.enabled_flag == 1]
        if params.get('company_id'):
            q.append(cls.company_id == params['company_id'])
        if params.get('certificate_type'):
            q.append(cls.certificate_type == params['certificate_type'])
        if params.get('certificate_status') is not None:
            q.append(cls.certificate_status == params['certificate_status'])
        if params.get('certificate_name'):
            name = params['certificate_name'].replace('%', '\\%').replace('_', '\\_')
            q.append(cls.certificate_name.like(f'%{name}%'))

        return await cls.get_list_by_page(q, params.get('page', 1), params.get('page_size', 10))


class Personnel(Base):
    """人员信息表"""
    __tablename__ = 'personnel'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True, comment='主键ID')
    company_id = Column(Integer, nullable=False, comment='公司ID')
    name = Column(String(100), nullable=False, comment='姓名')
    gender = Column(String(10), nullable=True, comment='性别')
    birth_date = Column(Date, nullable=True, comment='出生日期')
    id_card_no = Column(String(50), nullable=True, comment='身份证号码', index=True)
    id_card_path = Column(String(500), nullable=True, comment='身份证号码地址')
    is_principal = Column(SmallInteger, nullable=True, default=0, comment='是否公司负责人')
    education = Column(String(50), nullable=True, comment='学历')
    graduate_school = Column(String(200), nullable=True, comment='毕业院校')
    major = Column(String(100), nullable=True, comment='专业')
    educational_certificate_path = Column(String(100), nullable=True, comment='学历证书路径')
    work_years = Column(Integer, nullable=True, comment='工作年限')
    phone = Column(String(20), nullable=True, comment='手机号码')
    email = Column(String(100), nullable=True, comment='电子邮箱')
    is_full_time = Column(SmallInteger, nullable=True, default=1, comment='是否专职')
    employment_date = Column(Date, nullable=True, comment='入职日期')
    work_experience = Column(Text, nullable=True, comment='工作经历')
    project_experience = Column(Text, nullable=True, comment='项目经验')
    title = Column(String(50), nullable=True, comment='职称')
    work_start_date = Column(Date, nullable=True, comment='参加工作时间（匹配简历表“参加工作时间”）')
    resume_path = Column(String(500), nullable=True, comment='简历路径')
    labor_contract_path = Column(JSON, nullable=True, comment='劳动合同路径')
    social_security_path = Column(String(500), nullable=True, comment='社保证明路径')
    personnel_status = Column(SmallInteger, nullable=True, default=1, comment='人员状态:1-在职,0-离职,2-休假')
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now, comment='创建时间')
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    @classmethod
    async def get_list(cls, params: typing.Dict) -> typing.Dict[typing.Text, typing.Any]:
        """
        获取人员信息列表

        :param params: 查询参数
        :type params: typing.Dict
        :return: 分页数据
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        q = [cls.enabled_flag == 1]
        if params.get('company_id'):
            q.append(cls.company_id == params['company_id'])
        if params.get('name'):
            name = params['name'].replace('%', '\\%').replace('_', '\\_')
            q.append(cls.name.like(f'%{name}%'))
        if params.get('gender'):
            q.append(cls.gender == params['gender'])
        if params.get('personnel_status') is not None:
            q.append(cls.personnel_status == params['personnel_status'])
        if params.get('is_principal') is not None:
            q.append(cls.is_principal == params['is_principal'])
        if params.get('is_full_time') is not None:
            q.append(cls.is_full_time == params['is_full_time'])

        return await cls.get_list_by_page(q, params.get('page', 1), params.get('page_size', 10))


class PersonnelQualificationCertificate(Base):
    """员工资质证书表"""
    __tablename__ = 'personnel_qualification_certificate'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True, comment='主键ID')
    personnel_id = Column(Integer, nullable=False, comment='人员ID', index=True)
    personnel_name = Column(String(20), nullable=False, comment='人员名称', index=True)
    certificate_type = Column(String(100), nullable=False, comment='证书类型', index=True)
    certificate_title = Column(String(300), nullable=True, comment='岗位名称')
    certificate_full_name = Column(String(300), nullable=True, comment='证书全称')
    certificate_no = Column(String(100), nullable=False, comment='证书编号')
    certificate_level = Column(String(50), nullable=True, comment='证书等级')
    certificate_profession = Column(String(100), nullable=True, comment='证书专业')
    issue_organization = Column(String(200), nullable=True, comment='发证机构')
    issue_date = Column(Date, nullable=True, comment='发证日期')
    valid_until = Column(Date, nullable=True, comment='有效期至')
    certificate_status = Column(String(20), nullable=True, default='有效', comment='证书状态')
    profession_validity = Column(String(100), nullable=True, comment='专业有效期')
    training_institution = Column(String(200), nullable=True, comment='培训机构/评审组织')
    certificate_path = Column(String(500), nullable=True, comment='证书图片路径')
    remark = Column(Text, nullable=True, comment='备注')
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now, comment='创建时间')
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    @classmethod
    async def get_list(cls, params: typing.Dict) -> typing.Dict[typing.Text, typing.Any]:
        """
        获取员工资质证书列表

        :param params: 查询参数
        :type params: typing.Dict
        :return: 分页数据
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        q = [cls.enabled_flag == 1]
        if params.get('personnel_id'):
            q.append(cls.personnel_id == params['personnel_id'])
        if params.get('personnel_name'):
            name = params['personnel_name'].replace('%', '\\%').replace('_', '\\_')
            q.append(cls.personnel_name.like(f'%{name}%'))
        if params.get('certificate_type'):
            q.append(cls.certificate_type == params['certificate_type'])
        if params.get('certificate_status'):
            q.append(cls.certificate_status == params['certificate_status'])
        if params.get('certificate_no'):
            q.append(cls.certificate_no == params['certificate_no'])

        return await cls.get_list_by_page(q, params.get('page', 1), params.get('page_size', 10))


class BidSubmission(Base):
    """投标信息表"""
    __tablename__ = 'bid_submission'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True, comment='主键ID')
    project_id = Column(Integer, nullable=False, comment='项目ID', index=True)
    company_id = Column(Integer, nullable=False, comment='投标公司ID', index=True)
    survey_fee = Column(Numeric(12, 2), nullable=True, comment='勘察费(元/米钻探进尺)')
    design_fee_rate = Column(Numeric(5, 2), nullable=True, comment='设计费收费比例(%)')
    engineering_fee_rate = Column(Numeric(5, 2), nullable=True, comment='工程费优惠后的费率(%)')
    agent_id = Column(Integer, nullable=True, comment='委托人ID')
    agent_name = Column(String(10), nullable=True, comment='委托人姓名')
    agent_period = Column(Integer, nullable=True, comment='委托人 期限(天)')
    construction_qualification_level = Column(String(255), nullable=True, comment='施工资质等级')
    safety_certificate_no = Column(String(100), nullable=True, comment='安全生产许可证编号')
    safety_certificate_path = Column(String(100), nullable=True, comment='安全生产许可证路径')
    bid_bond = Column(Numeric(12, 2), nullable=True, comment='投标保证金(元)')
    bid_bond_remark = Column(String(200), nullable=True, comment='保证金说明')
    bid_status = Column(String(20), nullable=True, default='准备中', comment='投标状态', index=True)
    submission_date = Column(Date, nullable=True, comment='投标日期')
    bid_open_result = Column(Text, nullable=True, comment='开标结果')
    bid_document_path = Column(String(500), nullable=True, comment='投标文件路径')
    bid_sheet_path = Column(String(500), nullable=True, comment='唱标一览表路径')
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now, comment='创建时间')
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    @classmethod
    async def get_list(cls, params: typing.Dict) -> typing.Dict[typing.Text, typing.Any]:
        """
        获取投标信息列表

        :param params: 查询参数
        :type params: typing.Dict
        :return: 分页数据
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        q = [cls.enabled_flag == 1]
        if params.get('project_id'):
            q.append(cls.project_id == params['project_id'])
        if params.get('company_id'):
            q.append(cls.company_id == params['company_id'])
        if params.get('bid_status'):
            q.append(cls.bid_status == params['bid_status'])
        if params.get('submission_date'):
            q.append(cls.submission_date == params['submission_date'])

        return await cls.get_list_by_page(q, params.get('page', 1), params.get('page_size', 10))


class BidSubmissionPersonnel(Base):
    """投标绑定人员表"""
    __tablename__ = 'bid_submission_personnel'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True, comment='主键ID')
    project_id = Column(Integer, nullable=False, comment='项目ID', index=True)
    bid_submission_id = Column(Integer, nullable=False, comment='投标信息ID（关联具体投标）', index=True)
    personnel_id = Column(Integer, nullable=False, comment='人员ID', index=True)
    personnel_name = Column(String(50), nullable=False, comment='人员名称')
    post = Column(String(50), nullable=False, comment='项目指派岗位（与投标书岗位对应）')
    certificate_id = Column(Integer, nullable=False, comment='使用证书ID')
    is_full_time = Column(SmallInteger, nullable=False, default=1, comment='项目维度专职/兼职（投标书要求标注）')
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now, comment='创建时间')
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    @classmethod
    async def get_list(cls, params: typing.Dict) -> typing.Dict[typing.Text, typing.Any]:
        """
        获取投标绑定人员列表

        :param params: 查询参数
        :type params: typing.Dict
        :return: 分页数据
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        q = [cls.enabled_flag == 1]
        if params.get('project_id'):
            q.append(cls.project_id == params['project_id'])
        if params.get('bid_submission_id'):
            q.append(cls.bid_submission_id == params['bid_submission_id'])
        if params.get('personnel_id'):
            q.append(cls.personnel_id == params['personnel_id'])
        if params.get('post'):
            q.append(cls.post == params['post'])
        if params.get('is_full_time') is not None:
            q.append(cls.is_full_time == params['is_full_time'])

        return await cls.get_list_by_page(q, params.get('page', 1), params.get('page_size', 10))
