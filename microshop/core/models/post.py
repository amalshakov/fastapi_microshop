from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import UserRelationMixin


class Post(Base, UserRelationMixin):
    _user_back_populates: str = "posts"

    title: Mapped[str] = mapped_column(String(100))
    body: Mapped[str] = mapped_column(Text, default="", server_default="")

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}(id={self.id}, title={self.title!r}, "
            f"user_id={self.user_id})"
        )

    def __repr__(self) -> str:
        return str(self)
