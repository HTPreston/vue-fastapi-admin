import typing

from pydantic import BaseModel, Field
from datetime import date
from decimal import Decimal


class ProjectIn(BaseModel):
    """新增项目信息"""
    name: str = Field(..., description='项目名称')
    project_code: typing.Optional[str] = Field(None, description='项目编号')
    project_type: typing.Optional[str] = Field(None, description='项目类型')
    project_location: typing.Optional[str] = Field(None, description='项目地点')
    tender_organization: typing.Optional[str] = Field(None, description='招标单位')
    tender_agent: typing.Optional[str] = Field(None, description='招标代理机构')
    tender_number: typing.Optional[str] = Field(None, description='招标编号')
    tender_date: typing.Optional[date] = Field(None, description='招标日期')
    bid_open_date: typing.Optional[date] = Field(None, description='开标日期')
    project_status: typing.Optional[str] = Field('投标中', description='项目状态')
    project_cost: typing.Optional[Decimal] = Field(None, description='项目预计费用')


class ProjectUpdate(BaseModel):
    """更新项目信息"""
    id: int = Field(..., description='项目ID')
    name: typing.Optional[str] = Field(None, description='项目名称')
    project_code: typing.Optional[str] = Field(None, description='项目编号')
    project_type: typing.Optional[str] = Field(None, description='项目类型')
    project_location: typing.Optional[str] = Field(None, description='项目地点')
    tender_organization: typing.Optional[str] = Field(None, description='招标单位')
    tender_agent: typing.Optional[str] = Field(None, description='招标代理机构')
    tender_number: typing.Optional[str] = Field(None, description='招标编号')
    tender_date: typing.Optional[date] = Field(None, description='招标日期')
    bid_open_date: typing.Optional[date] = Field(None, description='开标日期')
    project_status: typing.Optional[str] = Field(None, description='项目状态')
    project_cost: typing.Optional[Decimal] = Field(None, description='项目预计费用')


class ProjectDel(BaseModel):
    """删除项目信息"""
    id: int = Field(..., description='项目ID')


class ProjectQuery(BaseModel):
    """查询项目信息"""
    name: typing.Optional[str] = Field(None, description='项目名称')
    project_code: typing.Optional[str] = Field(None, description='项目编号')
    project_type: typing.Optional[str] = Field(None, description='项目类型')
    project_status: typing.Optional[str] = Field(None, description='项目状态')
    tender_number: typing.Optional[str] = Field(None, description='招标编号')
    page: typing.Optional[int] = Field(1, description='页码')
    page_size: typing.Optional[int] = Field(10, description='每页数量')
