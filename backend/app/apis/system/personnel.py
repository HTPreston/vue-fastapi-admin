from app.corelibs.custom_router import APIRouter
from app.utils.response import HttpResponse

from app.schemas.system.personnel import (
    PersonnelIn, PersonnelUpdate, PersonnelDel, PersonnelQuery,
    PersonnelQualificationCertificateIn, PersonnelQualificationCertificateUpdate, 
    PersonnelQualificationCertificateDel, PersonnelQualificationCertificateQuery
)
from app.services.system.personnel import PersonnelService, PersonnelQualificationCertificateService


router = APIRouter()


# 人员信息相关接口
@router.post('/create', description="新增人员信息")
async def create_personnel(params: PersonnelIn):
    data = await PersonnelService.create(params)
    return await HttpResponse.success(data)


@router.post('/update', description="更新人员信息")
async def update_personnel(params: PersonnelUpdate):
    await PersonnelService.update(params)
    return await HttpResponse.success()


@router.post('/delete', description="删除人员信息")
async def delete_personnel(params: PersonnelDel):
    await PersonnelService.delete(params)
    return await HttpResponse.success()


@router.post('/list', description="获取人员信息列表")
async def get_personnel_list(params: PersonnelQuery):
    data = await PersonnelService.get_list(params)
    return await HttpResponse.success(data)


@router.post('/get', description="根据ID获取人员信息")
async def get_personnel_by_id(id: int):
    data = await PersonnelService.get_by_id(id)
    return await HttpResponse.success(data)


# 员工资质证书相关接口
@router.post('/qualification/create', description="新增员工资质证书")
async def create_personnel_qualification(params: PersonnelQualificationCertificateIn):
    data = await PersonnelQualificationCertificateService.create(params)
    return await HttpResponse.success(data)


@router.post('/qualification/update', description="更新员工资质证书")
async def update_personnel_qualification(params: PersonnelQualificationCertificateUpdate):
    await PersonnelQualificationCertificateService.update(params)
    return await HttpResponse.success()


@router.post('/qualification/delete', description="删除员工资质证书")
async def delete_personnel_qualification(params: PersonnelQualificationCertificateDel):
    await PersonnelQualificationCertificateService.delete(params)
    return await HttpResponse.success()


@router.post('/qualification/list', description="获取员工资质证书列表")
async def get_personnel_qualification_list(params: PersonnelQualificationCertificateQuery):
    data = await PersonnelQualificationCertificateService.get_list(params)
    return await HttpResponse.success(data)


@router.post('/qualification/get', description="根据ID获取员工资质证书")
async def get_personnel_qualification_by_id(id: int):
    data = await PersonnelQualificationCertificateService.get_by_id(id)
    return await HttpResponse.success(data)
