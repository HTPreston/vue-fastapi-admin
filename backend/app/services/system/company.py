import traceback
import typing

from loguru import logger
from app.models.system_models import CompanyInfo, CompanyQualificationCertificate
from app.schemas.system.company import (
    CompanyInfoIn, CompanyInfoUpdate, CompanyInfoDel, CompanyInfoQuery,
    CompanyQualificationCertificateIn, CompanyQualificationCertificateUpdate, 
    CompanyQualificationCertificateDel, CompanyQualificationCertificateQuery
)


class CompanyInfoService:
    """公司信息服务"""

    @staticmethod
    async def create(params: CompanyInfoIn) -> typing.Dict[typing.Text, typing.Any]:
        """
        新增公司信息

        :param params: 公司信息
        :type params: CompanyInfoIn
        :return: 创建的公司信息
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        try:
            data = await CompanyInfo.create(params.dict())
            return data
        except Exception as err:
            logger.error(traceback.format_exc())
            raise

    @staticmethod
    async def update(params: CompanyInfoUpdate) -> typing.Dict[typing.Text, typing.Any]:
        """
        更新公司信息

        :param params: 公司信息
        :type params: CompanyInfoUpdate
        :return: 更新后的公司信息
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        try:
            update_data = {k: v for k, v in params.dict().items() if v is not None and k != 'id'}
            result = await CompanyInfo.update({'id': params.id, **update_data})
            return result
        except Exception as err:
            logger.error(traceback.format_exc())
            raise

    @staticmethod
    async def delete(params: CompanyInfoDel) -> int:
        """
        删除公司信息

        :param params: 公司信息
        :type params: CompanyInfoDel
        :return: 影响行数
        :rtype: int
        """
        try:
            return await CompanyInfo.delete(params.id)
        except Exception as err:
            logger.error(traceback.format_exc())
            raise

    @staticmethod
    async def get_list(params: CompanyInfoQuery) -> typing.Dict[typing.Text, typing.Any]:
        """
        获取公司信息列表

        :param params: 查询参数
        :type params: CompanyInfoQuery
        :return: 分页数据
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        try:
            return await CompanyInfo.get_list(params.dict())
        except Exception as err:
            logger.error(traceback.format_exc())
            raise

    @staticmethod
    async def get_by_id(id: int) -> typing.Dict[typing.Text, typing.Any]:
        """
        根据ID获取公司信息

        :param id: 公司ID
        :type id: int
        :return: 公司信息
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        try:
            return await CompanyInfo.get(id, to_dict=True)
        except Exception as err:
            logger.error(traceback.format_exc())
            raise


class CompanyQualificationCertificateService:
    """公司资质证书服务"""

    @staticmethod
    async def create(params: CompanyQualificationCertificateIn) -> typing.Dict[typing.Text, typing.Any]:
        """
        新增公司资质证书

        :param params: 公司资质证书信息
        :type params: CompanyQualificationCertificateIn
        :return: 创建的公司资质证书
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        try:
            data = await CompanyQualificationCertificate.create(params.dict())
            return data
        except Exception as err:
            logger.error(traceback.format_exc())
            raise

    @staticmethod
    async def update(params: CompanyQualificationCertificateUpdate) -> typing.Dict[typing.Text, typing.Any]:
        """
        更新公司资质证书

        :param params: 公司资质证书信息
        :type params: CompanyQualificationCertificateUpdate
        :return: 更新后的公司资质证书
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        try:
            update_data = {k: v for k, v in params.dict().items() if v is not None and k != 'id'}
            result = await CompanyQualificationCertificate.update({'id': params.id, **update_data})
            return result
        except Exception as err:
            logger.error(traceback.format_exc())
            raise

    @staticmethod
    async def delete(params: CompanyQualificationCertificateDel) -> int:
        """
        删除公司资质证书

        :param params: 公司资质证书信息
        :type params: CompanyQualificationCertificateDel
        :return: 影响行数
        :rtype: int
        """
        try:
            return await CompanyQualificationCertificate.delete(params.id)
        except Exception as err:
            logger.error(traceback.format_exc())
            raise

    @staticmethod
    async def get_list(params: CompanyQualificationCertificateQuery) -> typing.Dict[typing.Text, typing.Any]:
        """
        获取公司资质证书列表

        :param params: 查询参数
        :type params: CompanyQualificationCertificateQuery
        :return: 分页数据
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        try:
            return await CompanyQualificationCertificate.get_list(params.dict())
        except Exception as err:
            logger.error(traceback.format_exc())
            raise

    @staticmethod
    async def get_by_id(id: int) -> typing.Dict[typing.Text, typing.Any]:
        """
        根据ID获取公司资质证书

        :param id: 证书ID
        :type id: int
        :return: 公司资质证书信息
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        try:
            return await CompanyQualificationCertificate.get(id, to_dict=True)
        except Exception as err:
            logger.error(traceback.format_exc())
            raise


