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

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "lastname": self.lastname,
            "firstname": self.firstname,
            "middlenames": self.middlenames,
            "initials": self.initials,
            "email": self.email,
            "institution": self.institution,
            "city": self.city,
            "country": self.country,
        }
