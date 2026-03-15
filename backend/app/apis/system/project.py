from app.corelibs.custom_router import APIRouter
from app.utils.response import HttpResponse
from app.schemas.system.project import (
    ProjectIn, ProjectUpdate, ProjectDel, ProjectQuery,
)
from app.services.system.project import ProjectService

router = APIRouter()


@router.post('/create', description="新增项目信息")
async def create(params: ProjectIn):
    data = await ProjectService.create(params)
    return await HttpResponse.success(data)


@router.post('/update', description="更新项目信息")
async def update(params: ProjectUpdate):
    await ProjectService.update(params)
    return await HttpResponse.success()


@router.post('/delete', description="删除项目信息")
async def delete(params: ProjectDel):
    await ProjectService.delete(params)
    return await HttpResponse.success()


@router.post('/list', description="获取项目信息列表")
async def get_list(params: ProjectQuery):
    data = await ProjectService.get_list(params)
    return await HttpResponse.success(data)


@router.post('/get', description="根据ID获取项目信息")
async def get_by_id(params: ProjectDel):
    data = await ProjectService.get_by_id(params.id)
    return await HttpResponse.success(data)
