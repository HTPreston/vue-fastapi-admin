import traceback
import typing

from loguru import logger
from app.models.system_models import BidSubmission
from app.schemas.system.bid_submission import (
    BidSubmissionIn, BidSubmissionUpdate, BidSubmissionDel, BidSubmissionQuery
)


class BidSubmissionService:
    """投标信息服务"""

    @staticmethod
    async def create(params: BidSubmissionIn) -> typing.Dict[typing.Text, typing.Any]:
        """
        新增投标信息

        :param params: 投标信息
        :type params: BidSubmissionIn
        :return: 创建的投标信息
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        try:
            data = await BidSubmission.create(params.dict())
            return data
        except Exception as err:
            logger.error(traceback.format_exc())
            raise

    @staticmethod
    async def update(params: BidSubmissionUpdate) -> typing.Dict[typing.Text, typing.Any]:
        """
        更新投标信息

        :param params: 投标信息
        :type params: BidSubmissionUpdate
        :return: 更新后的投标信息
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        try:
            update_data = {k: v for k, v in params.dict().items() if v is not None and k != 'id'}
            result = await BidSubmission.update({'id': params.id, **update_data})
            return result
        except Exception as err:
            logger.error(traceback.format_exc())
            raise

    @staticmethod
    async def delete(params: BidSubmissionDel) -> int:
        """
        删除投标信息

        :param params: 投标信息
        :type params: BidSubmissionDel
        :return: 影响行数
        :rtype: int
        """
        try:
            return await BidSubmission.delete(params.id)
        except Exception as err:
            logger.error(traceback.format_exc())
            raise

    @staticmethod
    async def get_list(params: BidSubmissionQuery) -> typing.Dict[typing.Text, typing.Any]:
        """
        获取投标信息列表

        :param params: 查询参数
        :type params: BidSubmissionQuery
        :return: 分页数据
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        try:
            return await BidSubmission.get_list(params.dict())
        except Exception as err:
            logger.error(traceback.format_exc())
            raise

    @staticmethod
    async def get_by_id(id: int) -> typing.Dict[typing.Text, typing.Any]:
        """
        根据ID获取投标信息

        :param id: 投标ID
        :type id: int
        :return: 投标信息
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        try:
            return await BidSubmission.get(id, to_dict=True)
        except Exception as err:
            logger.error(traceback.format_exc())
            raise