from typing import Annotated

from app.api.user.schemas import GuessRequest, LevelResponse, UserProfileResponse
from app.core.settings import settings
from app.database.models import Inactive, Level, User
from app.dependencies.db_dependency import DBDependency
from app.dependencies.redis_dependency import RedisDependency
from app.dependencies.responses import emptyresponse, okresponse
from fastapi import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import and_, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class PanoService:
    user = User
    level = Level
    inactive = Inactive

    def __init__(
        self,
        db: Annotated[DBDependency, Depends(DBDependency)],
        redis: Annotated[RedisDependency, Depends(RedisDependency)],
    ):
        self.db = db
        self.redis = redis

    async def _check_user(self, user_id: int, session: AsyncSession):
        user = await session.execute(select(self.user).where(self.user.id == user_id))
        user = user.scalar_one_or_none()
        if user:
            return user
        raise HTTPException(404, "User not found")

    async def profile(self, user_id: int):
        async with self.db.db_session() as session:
            user = await self._check_user(user_id, session)
            return UserProfileResponse.model_validate(user, from_attributes=True)

    async def get_panorama_unique(self, user_id: int):
        async with self.db.db_session() as session:
            user = await self._check_user(user_id, session)
            if user.count <= settings.max_count:
                level = await session.execute(
                    select(self.level)
                    .outerjoin(
                        self.inactive,
                        and_(
                            self.inactive.level_id == self.level.id,
                            self.inactive.user_id == user_id,
                        ),
                    )
                    .where(self.inactive.level_id is None)
                    .order_by(func.random())
                    .limit(1)
                )
                level = level.scalar_one_or_none()
                if level:
                    return LevelResponse(level_id=level.id, url=level.panorama_url)
                raise HTTPException(404, "New level not found")
            raise HTTPException(425, "Wait")

    async def get_panorama(self, user_id: int):
        async with self.db.db_session() as session:
            user = await self._check_user(user_id, session)
            if user.count <= settings.max_count:
                level = await session.execute(select(self.level).order_by(func.random()).limit(1))
                level = level.scalar_one_or_none()
                return LevelResponse(level_id=level.id, url=level.panorama_url)
            raise HTTPException(425, "Wait")

    async def submit_guess(self, user_id: int, guess: GuessRequest):
        async with self.db.db_session() as session:
            user = await self._check_user(user_id, session)
            level = await session.execute(select(self.level).where(self.level.id == guess.level))
            level = level.scalar_one_or_none()
            if level:
                await session.execute(
                    update(self.user).where(self.user.id == user_id).values(count=user.count + 1)
                )
                await session.commit()
                if level.room_num == guess.room_num:
                    return okresponse()
                raise HTTPException(400, "Wrong guess")
            raise HTTPException(404, "Level not found")

    async def set_user_notifications(self, user_id: int):
        async with self.db.db_session() as session:
            user = await self._check_user(user_id, session)
            await session.execute(
                update(self.user)
                .where(self.user.id == user_id)
                .values(notifications_bool=not user.notifications_bool)
            )
            await session.commit()
            return emptyresponse(200)
