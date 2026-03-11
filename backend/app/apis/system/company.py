from app.corelibs.custom_router import APIRouter
from app.utils.response import HttpResponse
from app.schemas.system.company import (
    CompanyInfoIn, CompanyInfoUpdate, CompanyInfoDel, CompanyInfoQuery,
    CompanyQualificationCertificateIn, CompanyQualificationCertificateUpdate, 
    CompanyQualificationCertificateDel, CompanyQualificationCertificateQuery,
)
from app.services.system.company import CompanyInfoService, CompanyQualificationCertificateService

router = APIRouter()


@router.post('/create', description="新增公司信息")
async def create(params: CompanyInfoIn):
    data = await CompanyInfoService.create(params)
    return await HttpResponse.success(data)


@router.post('/update', description="更新公司信息")
async def update(params: CompanyInfoUpdate):
    await CompanyInfoService.update(params)
    return await HttpResponse.success()


@router.post('/delete', description="删除公司信息")
async def delete(params: CompanyInfoDel):
    await CompanyInfoService.delete(params)
    return await HttpResponse.success()


@router.post('/list', description="获取公司信息列表")
async def get_list(params: CompanyInfoQuery):
    data = await CompanyInfoService.get_list(params)
    return await HttpResponse.success(data)


@router.post('/get', description="根据ID获取公司信息")
async def get_by_id(id: int):
    data = await CompanyInfoService.get_by_id(id)
    return await HttpResponse.success(data)


# 公司资质证书相关接口
@router.post('/qualification/create', description="新增公司资质证书")
async def create_qualification(params: CompanyQualificationCertificateIn):
    data = await CompanyQualificationCertificateService.create(params)
    return await HttpResponse.success(data)


@router.post('/qualification/update', description="更新公司资质证书")
async def update_qualification(params: CompanyQualificationCertificateUpdate):
    await CompanyQualificationCertificateService.update(params)
    return await HttpResponse.success()


@router.post('/qualification/delete', description="删除公司资质证书")
async def delete_qualification(params: CompanyQualificationCertificateDel):
    await CompanyQualificationCertificateService.delete(params)
    return await HttpResponse.success()


@router.post('/qualification/list', description="获取公司资质证书列表")
async def get_qualification_list(params: CompanyQualificationCertificateQuery):
    data = await CompanyQualificationCertificateService.get_list(params)
    return await HttpResponse.success(data)


@router.post('/qualification/get', description="根据ID获取公司资质证书")
async def get_qualification_by_id(id: int):
    data = await CompanyQualificationCertificateService.get_by_id(id)
    return await HttpResponse.success(data)





