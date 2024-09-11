from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import UserRelationMixin


class Profile(Base, UserRelationMixin):
    _user_id_unique: bool = True
    _user_back_populates: str = "profile"

    first_name: Mapped[str | None] = mapped_column(String(40))
    last_name: Mapped[str | None] = mapped_column(String(40))
    bio: Mapped[str | None]

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}(id={self.id}, "
            f"user_id={self.user_id})"
        )
