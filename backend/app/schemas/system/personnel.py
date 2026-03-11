import typing

from pydantic import BaseModel, Field
from datetime import date

class PersonnelIn(BaseModel):
    """新增人员信息"""
    company_id: int = Field(..., description='公司ID')
    name: typing.Optional[str] = Field(None, description='姓名')
    gender: typing.Optional[str] = Field(None, description='性别')
    birth_date: typing.Optional[date] = Field(None, description='出生日期')
    id_card_no: typing.Optional[str] = Field(None, description='身份证号码')
    id_card_path: typing.Optional[str] = Field(None, description='身份证号码地址')
    is_principal: typing.Optional[int] = Field(0, description='是否公司负责人')
    education: typing.Optional[str] = Field(None, description='学历')
    graduate_school: typing.Optional[str] = Field(None, description='毕业院校')
    major: typing.Optional[str] = Field(None, description='专业')
    educational_certificate_path: typing.Optional[str] = Field(None, description='学历证书路径')
    work_years: typing.Optional[int] = Field(None, description='工作年限')
    phone: typing.Optional[str] = Field(None, description='手机号码')
    email: typing.Optional[str] = Field(None, description='电子邮箱')
    is_full_time: typing.Optional[int] = Field(1, description='是否专职')
    employment_date: typing.Optional[date] = Field(None, description='入职日期')
    work_experience: typing.Optional[str] = Field(None, description='工作经历')
    project_experience: typing.Optional[str] = Field(None, description='项目经验')
    title: typing.Optional[str] = Field(None, description='职称')
    work_start_date: typing.Optional[date] = Field(None, description='参加工作时间（匹配简历表“参加工作时间”）')
    resume_path: typing.Optional[str] = Field(None, description='简历路径')
    labor_contract_path: typing.Optional[typing.List] = Field(None, description='劳动合同路径')
    social_security_path: typing.Optional[str] = Field(None, description='社保证明路径')
    personnel_status: typing.Optional[int] = Field(1, description='人员状态:1-在职,0-离职,2-休假')


class PersonnelUpdate(BaseModel):
    """更新人员信息"""
    id: int = Field(..., description='人员ID')
    company_id: typing.Optional[int] = Field(None, description='公司ID')
    name: typing.Optional[str] = Field(None, description='姓名')
    gender: typing.Optional[str] = Field(None, description='性别')
    birth_date: typing.Optional[date] = Field(None, description='出生日期')
    id_card_no: typing.Optional[str] = Field(None, description='身份证号码')
    id_card_path: typing.Optional[str] = Field(None, description='身份证号码地址')
    is_principal: typing.Optional[int] = Field(None, description='是否公司负责人')
    education: typing.Optional[str] = Field(None, description='学历')
    graduate_school: typing.Optional[str] = Field(None, description='毕业院校')
    major: typing.Optional[str] = Field(None, description='专业')
    educational_certificate_path: typing.Optional[str] = Field(None, description='学历证书路径')
    work_years: typing.Optional[int] = Field(None, description='工作年限')
    phone: typing.Optional[str] = Field(None, description='手机号码')
    email: typing.Optional[str] = Field(None, description='电子邮箱')
    is_full_time: typing.Optional[int] = Field(None, description='是否专职')
    employment_date: typing.Optional[date] = Field(None, description='入职日期')
    work_experience: typing.Optional[str] = Field(None, description='工作经历')
    project_experience: typing.Optional[str] = Field(None, description='项目经验')
    title: typing.Optional[str] = Field(None, description='职称')
    work_start_date: typing.Optional[date] = Field(None, description='参加工作时间（匹配简历表“参加工作时间”）')
    resume_path: typing.Optional[str] = Field(None, description='简历路径')
    labor_contract_path: typing.Optional[typing.List] = Field(None, description='劳动合同路径')
    social_security_path: typing.Optional[str] = Field(None, description='社保证明路径')
    personnel_status: typing.Optional[int] = Field(None, description='人员状态:1-在职,0-离职,2-休假')


class PersonnelDel(BaseModel):
    """删除人员信息"""
    id: int = Field(..., description='人员ID')


class PersonnelQuery(BaseModel):
    """查询人员信息"""
    company_id: typing.Optional[int] = Field(None, description='公司ID')
    name: typing.Optional[str] = Field(None, description='姓名')
    gender: typing.Optional[str] = Field(None, description='性别')
    personnel_status: typing.Optional[int] = Field(None, description='人员状态')
    is_principal: typing.Optional[int] = Field(None, description='是否公司负责人')
    is_full_time: typing.Optional[int] = Field(None, description='是否专职')
    page: typing.Optional[int] = Field(1, description='页码')
    page_size: typing.Optional[int] = Field(10, description='每页数量')


class PersonnelQualificationCertificateIn(BaseModel):
    """新增员工资质证书"""
    personnel_id: int = Field(..., description='人员ID')
    personnel_name: typing.Optional[str] = Field(None, description='人员名称')
    certificate_type: typing.Optional[str] = Field(None, description='证书类型')
    certificate_title: typing.Optional[str] = Field(None, description='岗位名称')
    certificate_full_name: typing.Optional[str] = Field(None, description='证书全称')
    certificate_no: typing.Optional[str] = Field(None, description='证书编号')
    certificate_level: typing.Optional[str] = Field(None, description='证书等级')
    certificate_profession: typing.Optional[str] = Field(None, description='证书专业')
    issue_organization: typing.Optional[str] = Field(None, description='发证机构')
    issue_date: typing.Optional[date] = Field(None, description='发证日期')
    valid_until: typing.Optional[date] = Field(None, description='有效期至')
    certificate_status: typing.Optional[str] = Field('有效', description='证书状态')
    profession_validity: typing.Optional[str] = Field(None, description='专业有效期')
    training_institution: typing.Optional[str] = Field(None, description='培训机构/评审组织')
    certificate_path: typing.Optional[str] = Field(None, description='证书图片路径')
    remark: typing.Optional[str] = Field(None, description='备注')


class PersonnelQualificationCertificateUpdate(BaseModel):
    """更新员工资质证书"""
    id: int = Field(..., description='证书ID')
    personnel_id: typing.Optional[int] = Field(None, description='人员ID')
    personnel_name: typing.Optional[str] = Field(None, description='人员名称')
    certificate_type: typing.Optional[str] = Field(None, description='证书类型')
    certificate_title: typing.Optional[str] = Field(None, description='岗位名称')
    certificate_full_name: typing.Optional[str] = Field(None, description='证书全称')
    certificate_no: typing.Optional[str] = Field(None, description='证书编号')
    certificate_level: typing.Optional[str] = Field(None, description='证书等级')
    certificate_profession: typing.Optional[str] = Field(None, description='证书专业')
    issue_organization: typing.Optional[str] = Field(None, description='发证机构')
    issue_date: typing.Optional[date] = Field(None, description='发证日期')
    valid_until: typing.Optional[date] = Field(None, description='有效期至')
    certificate_status: typing.Optional[str] = Field(None, description='证书状态')
    profession_validity: typing.Optional[str] = Field(None, description='专业有效期')
    training_institution: typing.Optional[str] = Field(None, description='培训机构/评审组织')
    certificate_path: typing.Optional[str] = Field(None, description='证书图片路径')
    remark: typing.Optional[str] = Field(None, description='备注')


class PersonnelQualificationCertificateDel(BaseModel):
    """删除员工资质证书"""
    id: int = Field(..., description='证书ID')


class PersonnelQualificationCertificateQuery(BaseModel):
    """查询员工资质证书"""
    personnel_id: typing.Optional[int] = Field(None, description='人员ID')
    personnel_name: typing.Optional[str] = Field(None, description='人员名称')
    certificate_type: typing.Optional[str] = Field(None, description='证书类型')
    certificate_status: typing.Optional[str] = Field(None, description='证书状态')
    certificate_no: typing.Optional[str] = Field(None, description='证书编号')
    page: typing.Optional[int] = Field(1, description='页码')
    page_size: typing.Optional[int] = Field(10, description='每页数量')