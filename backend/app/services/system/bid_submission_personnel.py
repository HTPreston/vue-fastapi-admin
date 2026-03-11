import traceback
import typing

from loguru import logger
from app.models.system_models import BidSubmissionPersonnel
from app.schemas.system.bid_submission_personnel import (
    BidSubmissionPersonnelIn, BidSubmissionPersonnelUpdate, 
    BidSubmissionPersonnelDel, BidSubmissionPersonnelQuery
)


class BidSubmissionPersonnelService:
    """投标绑定人员服务"""

    @staticmethod
    async def create(params: BidSubmissionPersonnelIn) -> typing.Dict[typing.Text, typing.Any]:
        """
        新增投标绑定人员

        :param params: 投标绑定人员信息
        :type params: BidSubmissionPersonnelIn
        :return: 创建的投标绑定人员
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        try:
            data = await BidSubmissionPersonnel.create(params.dict())
            return data
        except Exception as err:
            logger.error(traceback.format_exc())
            raise

    @staticmethod
    async def update(params: BidSubmissionPersonnelUpdate) -> typing.Dict[typing.Text, typing.Any]:
        """
        更新投标绑定人员

        :param params: 投标绑定人员信息
        :type params: BidSubmissionPersonnelUpdate
        :return: 更新后的投标绑定人员
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        try:
            update_data = {k: v for k, v in params.dict().items() if v is not None and k != 'id'}
            result = await BidSubmissionPersonnel.update({'id': params.id, **update_data})
            return result
        except Exception as err:
            logger.error(traceback.format_exc())
            raise

    @staticmethod
    async def delete(params: BidSubmissionPersonnelDel) -> int:
        """
        删除投标绑定人员

        :param params: 投标绑定人员信息
        :type params: BidSubmissionPersonnelDel
        :return: 影响行数
        :rtype: int
        """
        try:
            return await BidSubmissionPersonnel.delete(params.id)
        except Exception as err:
            logger.error(traceback.format_exc())
            raise

    @staticmethod
    async def get_list(params: BidSubmissionPersonnelQuery) -> typing.Dict[typing.Text, typing.Any]:
        """
        获取投标绑定人员列表

        :param params: 查询参数
        :type params: BidSubmissionPersonnelQuery
        :return: 分页数据
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        try:
            return await BidSubmissionPersonnel.get_list(params.dict())
        except Exception as err:
            logger.error(traceback.format_exc())
            raise

    @staticmethod
    async def get_by_id(id: int) -> typing.Dict[typing.Text, typing.Any]:
        """
        根据ID获取投标绑定人员

        :param id: 绑定人员ID
        :type id: int
        :return: 投标绑定人员信息
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        try:
            return await BidSubmissionPersonnel.get(id, to_dict=True)
        except Exception as err:
            logger.error(traceback.format_exc())
            raise