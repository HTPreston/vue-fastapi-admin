# -*- coding: utf-8 -*-
# @author: xiaobai
from fastapi import APIRouter

from app.apis.system import user, menu, roles, id_center, file

app_router = APIRouter()

# system
app_router.include_router(user.router, prefix="/user", tags=["user"])
app_router.include_router(menu.router, prefix="/menu", tags=["menu"])
app_router.include_router(roles.router, prefix="/roles", tags=["roles"])
app_router.include_router(id_center.router, prefix="/profile", tags=["id_center"])
app_router.include_router(file.router, prefix="/file", tags=["file"])
