from app.corelibs.custom_router import APIRouter
from app.utils.response import HttpResponse
from app.schemas.system.bid_submission import (
    BidSubmissionIn, BidSubmissionUpdate, BidSubmissionDel, BidSubmissionQuery
)
from app.services.system.bid_submission import BidSubmissionService

router = APIRouter()


@router.post('/create', description="新增投标信息")
async def create(params: BidSubmissionIn):
    data = await BidSubmissionService.create(params)
    return await HttpResponse.success(data)


@router.post('/update', description="更新投标信息")
async def update(params: BidSubmissionUpdate):
    await BidSubmissionService.update(params)
    return await HttpResponse.success()


@router.post('/delete', description="删除投标信息")
async def delete(params: BidSubmissionDel):
    await BidSubmissionService.delete(params)
    return await HttpResponse.success()


@router.post('/list', description="获取投标信息列表")
async def get_list(params: BidSubmissionQuery):
    data = await BidSubmissionService.get_list(params)
    return await HttpResponse.success(data)


@router.post('/get', description="根据ID获取投标信息")
async def get_by_id(id: int):
    data = await BidSubmissionService.get_by_id(id)
    return await HttpResponse.success(data)