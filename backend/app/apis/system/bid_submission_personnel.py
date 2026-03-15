from app.corelibs.custom_router import APIRouter
from app.utils.response import HttpResponse
from app.schemas.system.bid_submission_personnel import (
    BidSubmissionPersonnelIn, BidSubmissionPersonnelUpdate, 
    BidSubmissionPersonnelDel, BidSubmissionPersonnelQuery
)
from app.services.system.bid_submission_personnel import BidSubmissionPersonnelService

router = APIRouter()


@router.post('/create', description="新增投标绑定人员")
async def create(params: BidSubmissionPersonnelIn):
    data = await BidSubmissionPersonnelService.create(params)
    return await HttpResponse.success(data)


@router.post('/update', description="更新投标绑定人员")
async def update(params: BidSubmissionPersonnelUpdate):
    await BidSubmissionPersonnelService.update(params)
    return await HttpResponse.success()


@router.post('/delete', description="删除投标绑定人员")
async def delete(params: BidSubmissionPersonnelDel):
    await BidSubmissionPersonnelService.delete(params)
    return await HttpResponse.success()


@router.post('/list', description="获取投标绑定人员列表")
async def get_list(params: BidSubmissionPersonnelQuery):
    data = await BidSubmissionPersonnelService.get_list(params)
    return await HttpResponse.success(data)


@router.post('/get', description="根据ID获取投标绑定人员")
async def get_by_id(params: BidSubmissionPersonnelDel):
    data = await BidSubmissionPersonnelService.get_by_id(params.id)
    return await HttpResponse.success(data)