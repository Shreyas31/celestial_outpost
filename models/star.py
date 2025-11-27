from sqlalchemy.orm import Mapped
from .base import Base


class Star(Base):
    __tablename__ = "star"

    # Only storing basic data to display to the user.
    starname: Mapped[str]
    startype: Mapped[str]
    coordra: Mapped[float]
    coorddec: Mapped[float]
    color: Mapped[str]
    appmagnitude: Mapped[float]
    measurefilter: Mapped[str]
