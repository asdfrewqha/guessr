from typing import Annotated

from app.api.admin.services import AdminService
from app.dependencies.checks import check_user_token
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/set-admin/{user_id}")
async def set_admin(
    admin_id: Annotated[int, Depends(check_user_token)],
    user_id: int,
    service: Annotated[AdminService, Depends(AdminService)],
):
    return await service.set_admin(admin_id, user_id)
