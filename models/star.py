from sqlalchemy.orm import Mapped, relationship

from models.base import Base


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

    observations: Mapped[list["Observation"]] = relationship(back_populates="star")

    def coords_text(self) -> str:
        return f"{self.coordra:.3f}, {self.coorddec:.3f}"

    def magnitude_text(self) -> str:
        if not self.appmagnitude:
            return "No data"

        return f"{self.appmagnitude:.2f} mag ({self.measurefilter})"
