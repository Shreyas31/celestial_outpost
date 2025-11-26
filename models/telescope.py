from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Telescope(Base):
    __tablename__ = "telescope"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Can modify / add more -- this is just a template
    model: Mapped[str]
    aperture_size: Mapped[str]
    is_commercial: Mapped[bool]
    price_usd: Mapped[str]
