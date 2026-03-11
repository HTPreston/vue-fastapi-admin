import traceback
import typing

from loguru import logger
from app.models.system_models import Personnel
from app.schemas.system.personnel import (
    PersonnelIn, PersonnelUpdate, PersonnelDel, PersonnelQuery,
    PersonnelQualificationCertificateIn, PersonnelQualificationCertificateUpdate, 
    PersonnelQualificationCertificateDel, PersonnelQualificationCertificateQuery
)



class PersonnelService:
    """人员信息服务"""

    @staticmethod
    async def create(params: PersonnelIn) -> typing.Dict[typing.Text, typing.Any]:
        """
        新增人员信息

        :param params: 人员信息
        :type params: PersonnelIn
        :return: 创建的人员信息
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        try:
            data = await Personnel.create(params.dict())
            return data
        except Exception as err:
            logger.error(traceback.format_exc())
            raise

    @staticmethod
    async def update(params: PersonnelUpdate) -> typing.Dict[typing.Text, typing.Any]:
        """
        更新人员信息

        :param params: 人员信息
        :type params: PersonnelUpdate
        :return: 更新后的人员信息
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        try:
            update_data = {k: v for k, v in params.dict().items() if v is not None and k != 'id'}
            result = await Personnel.update({'id': params.id, **update_data})
            return result
        except Exception as err:
            logger.error(traceback.format_exc())
            raise

    @staticmethod
    async def delete(params: PersonnelDel) -> int:
        """
        删除人员信息

        :param params: 人员信息
        :type params: PersonnelDel
        :return: 影响行数
        :rtype: int
        """
        try:
            return await Personnel.delete(params.id)
        except Exception as err:
            logger.error(traceback.format_exc())
            raise

    @staticmethod
    async def get_list(params: PersonnelQuery) -> typing.Dict[typing.Text, typing.Any]:
        """
        获取人员信息列表

        :param params: 查询参数
        :type params: PersonnelQuery
        :return: 分页数据
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        try:
            return await Personnel.get_list(params.dict())
        except Exception as err:
            logger.error(traceback.format_exc())
            raise

    @staticmethod
    async def get_by_id(id: int) -> typing.Dict[typing.Text, typing.Any]:
        """
        根据ID获取人员信息

        :param id: 人员ID
        :type id: int
        :return: 人员信息
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        try:
            return await Personnel.get(id, to_dict=True)
        except Exception as err:
            logger.error(traceback.format_exc())
            raise


class PersonnelQualificationCertificateService:
    """员工资质证书服务"""

    @staticmethod
    async def create(params: PersonnelQualificationCertificateIn) -> typing.Dict[typing.Text, typing.Any]:
        """
        新增员工资质证书

        :param params: 员工资质证书信息
        :type params: PersonnelQualificationCertificateIn
        :return: 创建的员工资质证书
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        try:
            data = await PersonnelQualificationCertificate.create(params.dict())
            return data
        except Exception as err:
            logger.error(traceback.format_exc())
            raise

    @staticmethod
    async def update(params: PersonnelQualificationCertificateUpdate) -> typing.Dict[typing.Text, typing.Any]:
        """
        更新员工资质证书

        :param params: 员工资质证书信息
        :type params: PersonnelQualificationCertificateUpdate
        :return: 更新后的员工资质证书
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        try:
            update_data = {k: v for k, v in params.dict().items() if v is not None and k != 'id'}
            result = await PersonnelQualificationCertificate.update({'id': params.id, **update_data})
            return result
        except Exception as err:
            logger.error(traceback.format_exc())
            raise

    @staticmethod
    async def delete(params: PersonnelQualificationCertificateDel) -> int:
        """
        删除员工资质证书

        :param params: 员工资质证书信息
        :type params: PersonnelQualificationCertificateDel
        :return: 影响行数
        :rtype: int
        """
        try:
            return await PersonnelQualificationCertificate.delete(params.id)
        except Exception as err:
            logger.error(traceback.format_exc())
            raise

    @staticmethod
    async def get_list(params: PersonnelQualificationCertificateQuery) -> typing.Dict[typing.Text, typing.Any]:
        """
        获取员工资质证书列表

        :param params: 查询参数
        :type params: PersonnelQualificationCertificateQuery
        :return: 分页数据
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        try:
            return await PersonnelQualificationCertificate.get_list(params.dict())
        except Exception as err:
            logger.error(traceback.format_exc())
            raise

    @staticmethod
    async def get_by_id(id: int) -> typing.Dict[typing.Text, typing.Any]:
        """
        根据ID获取员工资质证书

        :param id: 证书ID
        :type id: int
        :return: 员工资质证书信息
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        try:
            return await PersonnelQualificationCertificate.get(id, to_dict=True)
        except Exception as err:
            logger.error(traceback.format_exc())
            raise
