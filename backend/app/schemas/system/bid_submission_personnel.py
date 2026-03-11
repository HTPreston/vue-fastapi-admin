import typing

from pydantic import BaseModel, Field


class BidSubmissionPersonnelIn(BaseModel):
    """新增投标绑定人员"""
    project_id: int = Field(..., description='项目ID')
    bid_submission_id: int = Field(..., description='投标信息ID（关联具体投标）')
    personnel_id: int = Field(..., description='人员ID')
    personnel_name: typing.Optional[str] = Field(None, description='人员名称')
    post: typing.Optional[str] = Field(None, description='项目指派岗位（与投标书岗位对应）')
    certificate_id: int = Field(..., description='使用证书ID')
    is_full_time: typing.Optional[int] = Field(1, description='项目维度专职/兼职（投标书要求标注）')


class BidSubmissionPersonnelUpdate(BaseModel):
    """更新投标绑定人员"""
    id: int = Field(..., description='绑定人员ID')
    project_id: typing.Optional[int] = Field(None, description='项目ID')
    bid_submission_id: typing.Optional[int] = Field(None, description='投标信息ID（关联具体投标）')
    personnel_id: typing.Optional[int] = Field(None, description='人员ID')
    personnel_name: typing.Optional[str] = Field(None, description='人员名称')
    post: typing.Optional[str] = Field(None, description='项目指派岗位（与投标书岗位对应）')
    certificate_id: typing.Optional[int] = Field(None, description='使用证书ID')
    is_full_time: typing.Optional[int] = Field(None, description='项目维度专职/兼职（投标书要求标注）')


class BidSubmissionPersonnelDel(BaseModel):
    """删除投标绑定人员"""
    id: int = Field(..., description='绑定人员ID')


class BidSubmissionPersonnelQuery(BaseModel):
    """查询投标绑定人员"""
    project_id: typing.Optional[int] = Field(None, description='项目ID')
    bid_submission_id: typing.Optional[int] = Field(None, description='投标信息ID（关联具体投标）')
    personnel_id: typing.Optional[int] = Field(None, description='人员ID')
    post: typing.Optional[str] = Field(None, description='项目指派岗位（与投标书岗位对应）')
    is_full_time: typing.Optional[int] = Field(None, description='项目维度专职/兼职（投标书要求标注）')
    page: typing.Optional[int] = Field(1, description='页码')
    page_size: typing.Optional[int] = Field(10, description='每页数量')