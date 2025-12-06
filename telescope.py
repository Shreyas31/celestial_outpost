from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional

from models.telescope import Telescope
from models.observation import Observation
from database import engine

telescope_bp = Blueprint("telescope", __name__, url_prefix="/telescope")


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


def render_home_page(**kwargs):
    stmt = select(Telescope).limit(25)
    with Session(engine) as session:
        telescopes = session.execute(stmt).scalars().all()

    return render_template(
        "telescope/home.html",
        telescopes=telescopes,
        **kwargs,
    )


# home page for telescope
@telescope_bp.route("/")
def home():
    return render_home_page()


# redirection for adding new telescope
@telescope_bp.route("/add", methods=["POST"])
def add_telescope():
    # NECESSARY FIELDS:
    name: Optional[str] = request.form.get("f_name")
    magnitude: Optional[int] = to_int_or_none(request.form.get("f_magnitude"))
    focuslength: Optional[int] = to_int_or_none(request.form.get("f_focuslength"))
    purchasable: bool = request.form.get("f_purchasable") is not None

    missing_params: list[str] = []
    if not name:
        missing_params.append("Name")
    if not magnitude:
        missing_params.append("Magnitude")
    if not focuslength:
        missing_params.append("Focus Length")

    if missing_params:
        return render_home_page(
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

        try:
            session.add(new_telescope)
            session.commit()
        except Exception as e:
            session.rollback()
            return render_home_page(error=f"Server error in adding telescope {e}.")

    return redirect(url_for("telescope.detail_telescope", id=new_telescope.id))


# searching for telescope
@telescope_bp.route("/search", methods=["POST"])
def search_telescope():
    searchid = to_int_or_none(request.form.get("f_search_id"))
    searchname = request.form.get("f_search_name")

    stmt = select(Telescope).where(
        (Telescope.id == searchid) | (Telescope.name == searchname)
    )
    with Session(engine) as session:
        telescope = session.execute(stmt).scalar_one_or_none()

    if not telescope:
        return render_home_page(error="Telescope queried not found.")

    return redirect(url_for("telescope.detail_telescope", id=telescope))


# display information for individual telescope
@telescope_bp.route("/<int:id>")
def detail_telescope(id):
    stmt = select(Telescope).where(Telescope.id == id)
    with Session(engine) as session:
        telescope = session.execute(stmt).scalar_one_or_none()

    if not telescope:
        return render_home_page(error="Telescope id not found.")

    # Get recent 50 observations made using this telescope
    stmt = (
        select(Observation)
        .where(Observation.telescope == telescope)
        .order_by(Observation.time.desc())
        .limit(50)
    )
    with Session(engine) as session:
        observations = session.execute(stmt).scalars().all()

    return render_template(
        "telescope/detail.html",
        telescope=telescope,
        observations=observations,
    )
