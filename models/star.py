from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Star(Base):
    __tablename__ = "star"

    # Only storing basic data to display to the user.
    id: Mapped[int] = mapped_column(primary_key=True)

    # Names of star (could have only scientific name)
    common_name: Mapped[str]
    scientific_name: Mapped[str]

    # Details of star
    apparent_magnitude: Mapped[float]
    color: Mapped[str]

    # Coordinates of star
    RA: Mapped[float]
    DEC: Mapped[float]
