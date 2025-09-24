from typing import Annotated

from app.api.admin.services import AdminService
from app.dependencies.checks import check_user_token
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/reset-count/all")
async def reset_count(
    user_id: Annotated[int, Depends(check_user_token)],
    service: Annotated[AdminService, Depends(AdminService)],
):
    return await service.reset_count(admin_id=user_id)
