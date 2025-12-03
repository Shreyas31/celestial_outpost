import os
from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import create_engine, select
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session
from typing import Optional

from models.telescope import Telescope

telescope_bp = Blueprint("telescope", __name__, url_prefix="/telescope")

url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),  # type: ignore  # noqa
    database=os.getenv("DB_NAME"),
    query={"client_encoding": "utf8"},
)

engine = create_engine(url)


# =============================================
# helper functions
# =============================================

# =============================================
# routes for human-facing web pages
# =============================================


# home page for telescope
@telescope_bp.route("/")
def home():
    with Session(engine) as session:
        telescopes = session.execute(select(Telescope)).scalars().all()

    return render_template(
        "telescope/home.html",
        telescopes=telescopes,
    )


def to_int_or_none(value: Optional[str]) -> Optional[int]:
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def to_float_or_none(value: Optional[str]) -> Optional[float]:
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


# redirection for adding new telescope
@telescope_bp.route("/add", methods=["POST"])
def add_telescope():
    # NECESSARY FIELDS:
    name: Optional[str] = request.form.get("f_name")
    magnitude: Optional[int] = to_int_or_none(request.form.get("f_magnitude"))
    focuslength: Optional[int] = to_int_or_none(request.form.get("f_focuslength"))
    purchasable: bool = request.form.get("f_purchasable") is not None

    if not name or not magnitude or not focuslength:
        missing_params: list[str] = []
        if not name:
            missing_params.append("Name")
        if not magnitude:
            missing_params.append("Magnitude")
        if not focuslength:
            missing_params.append("Focus Length")

        with Session(engine) as session:
            telescopes = session.execute(select(Telescope)).scalars().all()

        return render_template(
            "telescope/home.html",
            telescopes=telescopes,
            error=f"Invalid form input. Missing or invalid: {', '.join(missing_params)}",
        )

    # NON-NECESSARY FIELDS
    manufacturer: Optional[str] = request.form.get("f_manufacturer")
    aperture: Optional[int] = to_int_or_none(request.form.get("f_aperture"))
    fieldwidth: Optional[float] = to_float_or_none(request.form.get("f_fieldwidth"))
    fieldheight: Optional[float] = to_float_or_none(request.form.get("f_fieldheight"))
    length: Optional[int] = to_int_or_none(request.form.get("f_length"))
    weight: Optional[float] = to_float_or_none(request.form.get("f_weight"))
    imageurl: Optional[str] = request.form.get("f_imageurl")

    with Session(engine) as session:
        new_telescope = Telescope(
            name=name,
            manufacturer=manufacturer,
            focuslength=focuslength,
            purchasable=purchasable,
            aperture=aperture,
            magnitude=magnitude,
            fieldwidth=fieldwidth,
            fieldheight=fieldheight,
            length=length,
            weight=weight,
            imageurl=imageurl,
        )

        session.add(new_telescope)
        session.commit()

        return redirect(url_for("home"))


# searching for telescope
@telescope_bp.route("/search", methods=["POST"])
def search_telescope():
    searchid = int(request.form.get("t_search_id", default=0))
    searchname = request.form.get("t_search_name")

    with Session(engine) as session:
        stmt = select(Telescope).where(
            (Telescope.name == searchname) | (Telescope.id == searchid)
        )

        telescope = session.execute(stmt).scalar_one_or_none()

        if telescope:
            return redirect(f"/telescope/{telescope.id}")
        return redirect(
            url_for("home", error="Not found, Please enter a new telescope.")
        )


# display information for individual telescope
@telescope_bp.route("/<int:id>", methods=["GET", "POST"])
def telescope_information(id):

    with Session(engine) as session:
        telescope = session.execute(
            select(Telescope).where((Telescope.id == id))
        ).scalar_one_or_none()

    if telescope:
        return render_template("telescope/detail.html", telescope=telescope)

    return redirect(url_for("home", error="Not found, Please enter a new telescope."))
