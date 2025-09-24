import inflect
from app.database.mixins.id_mixins import IDMixin
from app.database.mixins.timestamp_mixins import TimestampsMixin
from app.database.utils import Role
from sqlalchemy import BigInteger, Boolean, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import (
    Mapped,
    declarative_base,
    declared_attr,
    mapped_column,
    relationship,
)

p = inflect.engine()


class Base:
    @declared_attr
    def __tablename__(cls):
        return p.plural(cls.__name__.lower())


Base = declarative_base(cls=Base)


class User(TimestampsMixin, Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.USER)
    notifications_bool: Mapped[bool] = mapped_column(Boolean, default=True)
    firstname: Mapped[str] = mapped_column(String, nullable=True)
    surname: Mapped[str] = mapped_column(String, nullable=True)
    grade: Mapped[str] = mapped_column(String, nullable=True)
    completed: Mapped[int] = mapped_column(Integer, default=0)
    count: Mapped[int] = mapped_column(Integer, default=0)

    levels = relationship("Inactive", back_populates="user", cascade="all, delete-orphan")


class Level(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    panorama_url: Mapped[str] = mapped_column(String, nullable=False)
    room_num: Mapped[int] = mapped_column(Integer, unique=True)


class Inactive(IDMixin, TimestampsMixin, Base):
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    level_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("levels.id", ondelete="CASCADE"), nullable=False
    )

    user = relationship("User", back_populates="levels")
