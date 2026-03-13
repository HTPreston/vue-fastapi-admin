import typing

from app.models.system_models import Personnel, PersonnelQualificationCertificate
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
        personnel = Personnel(**params.model_dump())
        await personnel.save()
        return personnel.to_dict()

    @staticmethod
    async def update(params: PersonnelUpdate) -> None:
        """
        更新人员信息

        :param params: 人员信息
        :type params: PersonnelUpdate
        :return: None
        """
        personnel = await Personnel.get(params.id)
        if not personnel:
            raise ValueError('人员不存在')
        update_data = params.model_dump(exclude={'id'}, exclude_unset=True)
        await personnel.update(update_data)

    @staticmethod
    async def delete(params: PersonnelDel) -> None:
        """
        删除人员信息

        :param params: 人员ID
        :type params: PersonnelDel
        :return: None
        """
        personnel = await Personnel.get(params.id)
        if not personnel:
            raise ValueError('人员不存在')
        await personnel.delete()

    @staticmethod
    async def get_list(params: PersonnelQuery) -> typing.Dict[typing.Text, typing.Any]:
        """
        获取人员信息列表

        :param params: 查询参数
        :type params: PersonnelQuery
        :return: 分页数据
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        return await Personnel.get_list(params.model_dump())

    @staticmethod
    async def get_by_id(id: int) -> typing.Dict[typing.Text, typing.Any]:
        """
        根据ID获取人员信息

        :param id: 人员ID
        :type id: int
        :return: 人员信息
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        personnel = await Personnel.get(id)
        if not personnel:
            raise ValueError('人员不存在')
        return personnel.to_dict()


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
        certificate = PersonnelQualificationCertificate(**params.model_dump())
        await certificate.save()
        return certificate.to_dict()

    @staticmethod
    async def update(params: PersonnelQualificationCertificateUpdate) -> None:
        """
        更新员工资质证书

        :param params: 员工资质证书信息
        :type params: PersonnelQualificationCertificateUpdate
        :return: None
        """
        certificate = await PersonnelQualificationCertificate.get(params.id)
        if not certificate:
            raise ValueError('证书不存在')
        update_data = params.model_dump(exclude={'id'}, exclude_unset=True)
        await certificate.update(update_data)

    @staticmethod
    async def delete(params: PersonnelQualificationCertificateDel) -> None:
        """
        删除员工资质证书

        :param params: 员工资质证书ID
        :type params: PersonnelQualificationCertificateDel
        :return: None
        """
        certificate = await PersonnelQualificationCertificate.get(params.id)
        if not certificate:
            raise ValueError('证书不存在')
        await certificate.delete()

    @staticmethod
    async def get_list(params: PersonnelQualificationCertificateQuery) -> typing.Dict[typing.Text, typing.Any]:
        """
        获取员工资质证书列表

        :param params: 查询参数
        :type params: PersonnelQualificationCertificateQuery
        :return: 分页数据
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        return await PersonnelQualificationCertificate.get_list(params.model_dump())

    @staticmethod
    async def get_by_id(id: int) -> typing.Dict[typing.Text, typing.Any]:
        """
        根据ID获取员工资质证书

        :param id: 证书ID
        :type id: int
        :return: 员工资质证书信息
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        certificate = await PersonnelQualificationCertificate.get(id)
        if not certificate:
            raise ValueError('证书不存在')
        return certificate.to_dict()
