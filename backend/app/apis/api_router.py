from fastapi import APIRouter

from app.apis.system import (user, menu, roles, id_center, file, company, 
                             personnel, bid_submission, bid_submission_personnel, project)

app_router = APIRouter()

# system
app_router.include_router(user.router, prefix="/user", tags=["user"])
app_router.include_router(menu.router, prefix="/menu", tags=["menu"])
app_router.include_router(roles.router, prefix="/roles", tags=["roles"])
app_router.include_router(id_center.router, prefix="/profile", tags=["id_center"])
app_router.include_router(file.router, prefix="/file", tags=["file"])
app_router.include_router(company.router, prefix="/company", tags=["company"])
app_router.include_router(personnel.router, prefix="/personnel", tags=["personnel"])
app_router.include_router(project.router, prefix="/project", tags=["project"])
app_router.include_router(bid_submission.router, prefix="/bid_submission", tags=["bid_submission"])
app_router.include_router(bid_submission_personnel.router, prefix="/bid_submission_personnel", 
                          tags=["bid_submission_personnel"])
