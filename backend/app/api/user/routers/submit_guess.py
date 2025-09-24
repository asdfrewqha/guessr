from typing import Annotated

from app.api.user.schemas import GuessRequest
from app.api.user.services import PanoService
from app.dependencies.checks import check_user_token
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/submit-guess")
async def submit_guess(
    user_id: Annotated[int, Depends(check_user_token)],
    service: Annotated[PanoService, Depends(PanoService)],
    guess: GuessRequest,
):
    return await service.submit_guess(user_id, guess)
