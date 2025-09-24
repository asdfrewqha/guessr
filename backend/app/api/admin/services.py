from typing import Annotated

from app.core.settings import settings
from app.database.models import User
from app.database.utils import Role
from app.dependencies.db_dependency import DBDependency
from app.dependencies.redis_dependency import RedisDependency
from app.dependencies.responses import okresponse
from fastapi import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class AdminService:
    user = User

    def __init__(
        self,
        db: Annotated[DBDependency, Depends(DBDependency)],
        redis: Annotated[RedisDependency, Depends(RedisDependency)],
    ) -> None:
        self.db = db
        self.redis = redis

    async def _check_user(self, user_id: int, session: AsyncSession):
        user = await session.execute(select(self.user).where(self.user.id == user_id))
        user = user.scalar_one_or_none()
        if user:
            if user.role == Role.ADMIN:
                return user
            raise HTTPException(403, "Forbidden")
        raise HTTPException(404, "User not found")

    async def set_admin(self, admin_id: int, user_id: int):
        if str(admin_id) == settings.admin_id.get_secret_value():
            async with self.db.db_session() as session:
                await session.execute(
                    update(self.user).where(self.user.id == user_id).values(role=Role.ADMIN)
                )
                await session.commit()
                return okresponse()
        raise HTTPException(403, "Forbidden")

    async def send_message_all(self, admin_id: int):
        async with self.db.db_session() as session:
            user = await self._check_user(admin_id, session)
            users = await session.execute(select(self.user.id).where(self.user.role == Role.USER))
            users = users.scalars().all()

    async def reset_count(self, admin_id: int):
        async with self.db.db_session() as session:
            user = await self._check_user(admin_id, session)
            await session.execute(
                update(self.user).where(self.user.role == Role.USER).values(count=0)
            )
            return okresponse()
