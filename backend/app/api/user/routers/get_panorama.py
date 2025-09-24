from typing import Annotated

from app.api.user.schemas import LevelResponse
from app.api.user.services import PanoService
from app.dependencies.checks import check_user_token
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/get-panorama", response_model=LevelResponse)
async def get_panorama(
    user_id: Annotated[int, Depends(check_user_token)],
    service: Annotated[PanoService, Depends(PanoService)],
):
    return await service.get_panorama(user_id=user_id)
