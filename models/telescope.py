from sqlalchemy.orm import Mapped

from .base import Base


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
