from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime

from models.base import Base

# from models.user import User
# from models.star import Star
# from models.telescope import Telescope


class Observation(Base):
    __tablename__ = "observation"

    userid: Mapped[int] = mapped_column(ForeignKey("user.id"))
    starid: Mapped[int] = mapped_column(ForeignKey("star.id"))
    telescopeid: Mapped[int] = mapped_column(ForeignKey("telescope.id"))

    # relationships

    user: Mapped["User"] = relationship(back_populates="observations")
    star: Mapped["Star"] = relationship(back_populates="observations")
    telescope: Mapped["Telescope"] = relationship(back_populates="observations")

    time: Mapped[datetime]
    city: Mapped[str]
    country: Mapped[str]
