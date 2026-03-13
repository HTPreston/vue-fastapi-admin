import typing

from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


class MenuIn(BaseModel):
    id: typing.Optional[int] = Field(None, description='主键ID')
    parent_id: typing.Optional[int] = Field(None, description='父级id')
    path: str = Field(..., description='菜单路径')
    name: typing.Optional[str] = Field(None, description='菜单名称')
    component: typing.Optional[str] = Field(None, description='组件路径')
    title: typing.Optional[str] = Field(None, description='title')
    isLink: typing.Optional[int] = Field(0, description='开启外链条件，`1、isLink: true 2、链接地址不为空（meta.isLink） 3、isIframe: false`')
    isHide: typing.Optional[int] = Field(0, description='菜单是否隐藏（菜单不显示在界面，但可以进行跳转）')
    icon: typing.Optional[str] = Field(None, description='图标')
    isKeepAlive: typing.Optional[int] = Field(None, description='菜单是否缓存')
    isAffix: typing.Optional[int] = Field(None, description='固定标签')
    isIframe: typing.Optional[int] = Field(None, description='是否内嵌')
    sort: typing.Optional[int] = Field(None, description='排序')
    active_menu: typing.Optional[str] = Field(None, description='显示页签')
    menu_type: typing.Optional[int] = Field(10, description='菜单类型')
    redirect: typing.Optional[str] = Field(None, description='重定向')


class MenuUpdate(MenuIn):
    pass


class MenuDel(BaseModel):
    id: int = Field(..., title="id", description='id')


class MenuViews(BaseModel):
    menu_id: int = Field(..., title="id", description='菜单id')


class Menu(BaseSchema):
    name: typing.Optional[str] = Field(None, description='组件名称')
