import typing

from pydantic import BaseModel, Field
from datetime import date


class BidSubmissionIn(BaseModel):
    """新增投标信息"""
    project_id: int = Field(..., description='项目ID')
    company_id: int = Field(..., description='投标公司ID')
    survey_fee: typing.Optional[float] = Field(None, description='勘察费(元/米钻探进尺)')
    design_fee_rate: typing.Optional[float] = Field(None, description='设计费收费比例(%)')
    engineering_fee_rate: typing.Optional[float] = Field(None, description='工程费优惠后的费率(%)')
    agent_id: typing.Optional[int] = Field(None, description='委托人ID')
    agent_name: typing.Optional[str] = Field(None, description='委托人姓名')
    agent_period: typing.Optional[int] = Field(None, description='委托人 期限(天)')
    construction_qualification_level: typing.Optional[str] = Field(None, description='施工资质等级')
    safety_certificate_no: typing.Optional[str] = Field(None, description='安全生产许可证编号')
    safety_certificate_path: typing.Optional[str] = Field(None, description='安全生产许可证路径')
    bid_bond: typing.Optional[float] = Field(None, description='投标保证金(元)')
    bid_bond_remark: typing.Optional[str] = Field(None, description='保证金说明')
    bid_status: typing.Optional[str] = Field('准备中', description='投标状态')
    submission_date: typing.Optional[date] = Field(None, description='投标日期')
    bid_open_result: typing.Optional[str] = Field(None, description='开标结果')
    bid_document_path: typing.Optional[str] = Field(None, description='投标文件路径')
    bid_sheet_path: typing.Optional[str] = Field(None, description='唱标一览表路径')


class BidSubmissionUpdate(BaseModel):
    """更新投标信息"""
    id: int = Field(..., description='投标ID')
    project_id: typing.Optional[int] = Field(None, description='项目ID')
    company_id: typing.Optional[int] = Field(None, description='投标公司ID')
    survey_fee: typing.Optional[float] = Field(None, description='勘察费(元/米钻探进尺)')
    design_fee_rate: typing.Optional[float] = Field(None, description='设计费收费比例(%)')
    engineering_fee_rate: typing.Optional[float] = Field(None, description='工程费优惠后的费率(%)')
    agent_id: typing.Optional[int] = Field(None, description='委托人ID')
    agent_name: typing.Optional[str] = Field(None, description='委托人姓名')
    agent_period: typing.Optional[int] = Field(None, description='委托人 期限(天)')
    construction_qualification_level: typing.Optional[str] = Field(None, description='施工资质等级')
    safety_certificate_no: typing.Optional[str] = Field(None, description='安全生产许可证编号')
    safety_certificate_path: typing.Optional[str] = Field(None, description='安全生产许可证路径')
    bid_bond: typing.Optional[float] = Field(None, description='投标保证金(元)')
    bid_bond_remark: typing.Optional[str] = Field(None, description='保证金说明')
    bid_status: typing.Optional[str] = Field(None, description='投标状态')
    submission_date: typing.Optional[date] = Field(None, description='投标日期')
    bid_open_result: typing.Optional[str] = Field(None, description='开标结果')
    bid_document_path: typing.Optional[str] = Field(None, description='投标文件路径')
    bid_sheet_path: typing.Optional[str] = Field(None, description='唱标一览表路径')


class BidSubmissionDel(BaseModel):
    """删除投标信息"""
    id: int = Field(..., description='投标ID')


class BidSubmissionQuery(BaseModel):
    """查询投标信息"""
    project_id: typing.Optional[int] = Field(None, description='项目ID')
    company_id: typing.Optional[int] = Field(None, description='投标公司ID')
    bid_status: typing.Optional[str] = Field(None, description='投标状态')
    submission_date: typing.Optional[date] = Field(None, description='投标日期')
    page: typing.Optional[int] = Field(1, description='页码')
    page_size: typing.Optional[int] = Field(10, description='每页数量')