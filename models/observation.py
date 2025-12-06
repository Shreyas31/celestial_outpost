from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime

from models.base import Base


class Observation(Base):
    __tablename__ = "observation"

    userid: Mapped[int] = mapped_column(ForeignKey("user.id"))
    starid: Mapped[int] = mapped_column(ForeignKey("star.id"))
    telescopeid: Mapped[int] = mapped_column(ForeignKey("telescope.id"))

    # relationships

    user: Mapped["User"] = relationship(
        back_populates="observations",
        lazy="joined",
    )
    star: Mapped["Star"] = relationship(
        back_populates="observations",
        lazy="joined",
    )
    telescope: Mapped["Telescope"] = relationship(
        back_populates="observations", lazy="joined"
    )

    time: Mapped[datetime]
    city: Mapped[str]
    country: Mapped[str]
