from sqlalchemy.orm import Mapped, relationship

from models.base import Base


class Telescope(Base):
    __tablename__ = "telescope"

    name: Mapped[str]
    manufacturer: Mapped[str]
    aperture: Mapped[int]
    magnitude: Mapped[float]
    focuslength: Mapped[int]
    fieldwidth: Mapped[float]
    fieldheight: Mapped[float]
    length: Mapped[int]
    weight: Mapped[float]
    purchasable: Mapped[bool]
    imageurl: Mapped[str]

    observations: Mapped[list["Observation"]] = relationship(back_populates="telescope")

    def fullname(self) -> str:
        return f"{self.manufacturer} {self.name}"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "manufacturer": self.manufacturer,
            "aperture": self.aperture,
            "magnitude": self.magnitude,
            "focuslength": self.focuslength,
            "fieldwidth": self.fieldwidth,
            "fieldheight": self.fieldheight,
            "length": self.length,
            "weight": self.weight,
            "purchasable": self.purchasable,
            "imageurl": self.imageurl,
        }
