import typing

from pydantic import BaseModel, Field
from datetime import date


class CompanyInfoIn(BaseModel):
    """新增公司信息"""
    name: typing.Optional[str] = Field(None, description='公司名称')
    short_name: typing.Optional[str] = Field(None, description='公司简称')
    english_name: typing.Optional[str] = Field(None, description='英文名称')
    credit_code: typing.Optional[str] = Field(None, description='统一社会信用代码')
    legal_representative: typing.Optional[str] = Field(None, description='法人代表人')
    registered_capital: typing.Optional[int] = Field(None, description='注册资本')
    establishment_date: typing.Optional[date] = Field(None, description='成立日期')
    business_term: typing.Optional[str] = Field(None, description='经营期限')
    company_type: typing.Optional[str] = Field(None, description='企业类型')
    business_scope: typing.Optional[str] = Field(None, description='经营范围')
    registered_address: typing.Optional[str] = Field(None, description='注册地址')
    office_address: typing.Optional[str] = Field(None, description='办公地址')
    postal_code: typing.Optional[str] = Field(None, description='邮政编码')
    contact_phone: typing.Optional[str] = Field(None, description='联系电话')
    fax: typing.Optional[str] = Field(None, description='传真号码')
    website: typing.Optional[str] = Field(None, description='公司网址')
    email: typing.Optional[str] = Field(None, description='电子邮箱')
    personnel_reserve: typing.Optional[typing.List] = Field(None, description='人员储备')
    bank_name: typing.Optional[str] = Field(None, description='开户银行')
    bank_account: typing.Optional[str] = Field(None, description='银行账号')
    business_license_path: typing.Optional[str] = Field(None, description='营业执照图片路径')
    deposit_account_path: typing.Optional[str] = Field(None, description='存款账户图片路径')
    status: typing.Optional[int] = Field(1, description='状态:1-正常,0-停用')


class CompanyInfoUpdate(BaseModel):
    """更新公司信息"""
    id: int = Field(..., description='公司id')
    name: typing.Optional[str] = Field(None, description='公司名称')
    short_name: typing.Optional[str] = Field(None, description='公司简称')
    english_name: typing.Optional[str] = Field(None, description='英文名称')
    credit_code: typing.Optional[str] = Field(None, description='统一社会信用代码')
    legal_representative: typing.Optional[str] = Field(None, description='法人代表人')
    registered_capital: typing.Optional[int] = Field(None, description='注册资本')
    establishment_date: typing.Optional[date] = Field(None, description='成立日期')
    business_term: typing.Optional[str] = Field(None, description='经营期限')
    company_type: typing.Optional[str] = Field(None, description='企业类型')
    business_scope: typing.Optional[str] = Field(None, description='经营范围')
    registered_address: typing.Optional[str] = Field(None, description='注册地址')
    office_address: typing.Optional[str] = Field(None, description='办公地址')
    postal_code: typing.Optional[str] = Field(None, description='邮政编码')
    contact_phone: typing.Optional[str] = Field(None, description='联系电话')
    fax: typing.Optional[str] = Field(None, description='传真号码')
    website: typing.Optional[str] = Field(None, description='公司网址')
    email: typing.Optional[str] = Field(None, description='电子邮箱')
    personnel_reserve: typing.Optional[typing.List] = Field(None, description='人员储备')
    bank_name: typing.Optional[str] = Field(None, description='开户银行')
    bank_account: typing.Optional[str] = Field(None, description='银行账号')
    business_license_path: typing.Optional[str] = Field(None, description='营业执照图片路径')
    deposit_account_path: typing.Optional[str] = Field(None, description='存款账户图片路径')
    status: typing.Optional[int] = Field(None, description='状态:1-正常,0-停用')


class CompanyInfoDel(BaseModel):
    """删除公司信息"""
    id: int = Field(..., description='公司id')


class CompanyInfoQuery(BaseModel):
    """查询公司信息"""
    name: typing.Optional[str] = Field(None, description='公司名称')
    status: typing.Optional[int] = Field(None, description='状态')
    page: typing.Optional[int] = Field(1, description='页码')
    page_size: typing.Optional[int] = Field(10, description='每页数量')


class CompanyQualificationCertificateIn(BaseModel):
    """新增公司资质证书"""
    company_id: int = Field(..., description='公司ID')
    certificate_type: typing.Optional[str] = Field(None, description='资质类型')
    certificate_level: typing.Optional[str] = Field(None, description='资质等级')
    certificate_no: typing.Optional[str] = Field(None, description='证书编号')
    certificate_name: typing.Optional[str] = Field(None, description='证书全称')
    issue_authority: typing.Optional[str] = Field(None, description='发证机关')
    issue_date: typing.Optional[date] = Field(None, description='发证日期')
    valid_until: typing.Optional[date] = Field(None, description='有效期至')
    certificate_status: typing.Optional[int] = Field(1, description='证书状态:1-有效,0-无效,2-即将到期')
    certificate_path: typing.Optional[str] = Field(None, description='证书图片路径')
    remark: typing.Optional[str] = Field(None, description='备注')


class CompanyQualificationCertificateUpdate(BaseModel):
    """更新公司资质证书"""
    id: int = Field(..., description='证书ID')
    company_id: typing.Optional[int] = Field(None, description='公司ID')
    certificate_type: typing.Optional[str] = Field(None, description='资质类型')
    certificate_level: typing.Optional[str] = Field(None, description='资质等级')
    certificate_no: typing.Optional[str] = Field(None, description='证书编号')
    certificate_name: typing.Optional[str] = Field(None, description='证书全称')
    issue_authority: typing.Optional[str] = Field(None, description='发证机关')
    issue_date: typing.Optional[date] = Field(None, description='发证日期')
    valid_until: typing.Optional[date] = Field(None, description='有效期至')
    certificate_status: typing.Optional[int] = Field(None, description='证书状态:1-有效,0-无效,2-即将到期')
    certificate_path: typing.Optional[str] = Field(None, description='证书图片路径')
    remark: typing.Optional[str] = Field(None, description='备注')


class CompanyQualificationCertificateDel(BaseModel):
    """删除公司资质证书"""
    id: int = Field(..., description='证书ID')


class CompanyQualificationCertificateQuery(BaseModel):
    """查询公司资质证书"""
    company_id: typing.Optional[int] = Field(None, description='公司ID')
    certificate_type: typing.Optional[str] = Field(None, description='资质类型')
    certificate_status: typing.Optional[int] = Field(None, description='证书状态')
    certificate_name: typing.Optional[str] = Field(None, description='证书全称')
    page: typing.Optional[int] = Field(1, description='页码')
    page_size: typing.Optional[int] = Field(10, description='每页数量')





