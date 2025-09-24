from typing import Annotated

from app.api.auth.schemas import InitData
from app.api.auth.services import UserService
from fastapi import APIRouter, Depends, Form
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/login")
async def telegram_auth(
    service: Annotated[UserService, Depends(UserService)], initData: str = Form(...)
):
    tokens = await service.login(InitData(initData=initData))
    response = JSONResponse({"message": str(tokens[1]), "status": "success"})
    response.set_cookie(
        "access_token",
        tokens[0].access_token,
        httponly=True,
        secure=True,
        samesite="none",
    )
    response.set_cookie(
        "refresh_token",
        tokens[0].refresh_token,
        httponly=True,
        secure=True,
        samesite="none",
    )
    return response
