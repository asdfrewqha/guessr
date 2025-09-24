from typing import Annotated

from app.api.admin.services import AdminService
from app.dependencies.checks import check_user_token
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/send-message/all")
async def send_message_all(
    user_id: Annotated[int, Depends(check_user_token)],
    service: Annotated[AdminService, Depends(AdminService)],
):
    return await service.send_message_all(admin_id=user_id)
