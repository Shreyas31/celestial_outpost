from typing import Sequence, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime

from models.base import Base
from models.user import User
from models.star import Star
from models.telescope import Telescope


class Observation(Base):
    __tablename__ = "observation"

    userid: Mapped[int] = mapped_column(ForeignKey("user.id"))
    starid: Mapped[int] = mapped_column(ForeignKey("star.id"))
    telescopeid: Mapped[int] = mapped_column(ForeignKey("telescope.id"))

    # relationships

    user: Mapped[User] = relationship(
        back_populates="observations",
        lazy="joined",
    )
    star: Mapped[Star] = relationship(
        back_populates="observations",
        lazy="joined",
    )
    telescope: Mapped[Telescope] = relationship(
        back_populates="observations", lazy="joined"
    )

    time: Mapped[datetime]
    city: Mapped[str]
    country: Mapped[str]

    def to_dict(self, exclude: Optional[Sequence[str]] = None) -> dict:
        d = {
            "id": self.id,
            "userid": self.userid,
            "user_name": self.user.get_full_name(),
            "starid": self.starid,
            "star_name": self.star.starname,
            "telescopeid": self.telescopeid,
            "telescope_name": self.telescope.name,
            "time": self.time,
            "city": self.city,
            "country": self.country,
        }

        if exclude:
            for ex in exclude:
                if ex in d:
                    del d[ex]

        return d
