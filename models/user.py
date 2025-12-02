from sqlalchemy.orm import Mapped, relationship

from models.base import Base


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

    observations: Mapped[list["Observation"]] = relationship(back_populates="user")

    def get_full_name(self) -> str:
        return f"{self.firstname} {self.lastname}"
