from typing import Optional

from app.database.utils import Role
from pydantic import BaseModel, ConfigDict


class UserProfileResponse(BaseModel):
    id: int
    username: str
    name: str
    role: Role
    notifications_bool: bool
    firstname: Optional[str] = None
    surname: Optional[str] = None
    grade: Optional[str] = None
    completed: int
    count: int

    model_config = ConfigDict(arbitrary_types_allowed=True)


class LevelResponse(BaseModel):
    level_id: int
    url: str


class GuessRequest(BaseModel):
    level: int
    room_num: int
