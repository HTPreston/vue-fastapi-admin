import typing

from app.models.system_models import Project
from app.schemas.system.project import ProjectIn, ProjectUpdate, ProjectDel, ProjectQuery


class ProjectService:
    """项目服务类"""

    @staticmethod
    async def create(params: ProjectIn) -> typing.Dict[typing.Text, typing.Any]:
        """
        新增项目

        :param params: 项目信息
        :type params: ProjectIn
        :return: 项目信息
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        project = Project(**params.model_dump())
        await project.save()
        return project.to_dict()

    @staticmethod
    async def update(params: ProjectUpdate) -> None:
        """
        更新项目

        :param params: 项目信息
        :type params: ProjectUpdate
        :return: None
        """
        project = await Project.get(params.id)
        if not project:
            raise ValueError('项目不存在')
        update_data = params.model_dump(exclude={'id'}, exclude_unset=True)
        await project.update(update_data)

    @staticmethod
    async def delete(params: ProjectDel) -> None:
        """
        删除项目

        :param params: 项目ID
        :type params: ProjectDel
        :return: None
        """
        project = await Project.get(params.id)
        if not project:
            raise ValueError('项目不存在')
        await project.delete()

    @staticmethod
    async def get_list(params: ProjectQuery) -> typing.Dict[typing.Text, typing.Any]:
        """
        获取项目列表

        :param params: 查询参数
        :type params: ProjectQuery
        :return: 分页数据
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        return await Project.get_list(params.model_dump())

    @staticmethod
    async def get_by_id(id: int) -> typing.Dict[typing.Text, typing.Any]:
        """
        根据ID获取项目

        :param id: 项目ID
        :type id: int
        :return: 项目信息
        :rtype: typing.Dict[typing.Text, typing.Any]
        """
        project = await Project.get(id)
        if not project:
            raise ValueError('项目不存在')
        return project.to_dict()
