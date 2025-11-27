from sqlalchemy.orm import Mapped
from .base import Base


class User(Base):
    __tablename__ = "user"

    lastname: Mapped[str]
    firstname: Mapped[str]
    middlenames: Mapped[str]
    initials: Mapped[str]
    email: Mapped[str]
    institution: Mapped[str]
    city: Mapped[str]
    country: Mapped[str]

    def get_full_name(self) -> str:
        return f"{self.firstname} {self.lastname}"
