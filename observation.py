from datetime import datetime

from flask import Blueprint, render_template, request
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import engine

from models.observation import Observation
from models.user import User
from models.telescope import Telescope
from starutils import find_existing_or_create_star

observation_bp = Blueprint("observation", __name__, url_prefix="/observation")


def render_home_page(**kwargs):
    stmt = select(Observation).order_by(Observation.time.desc()).limit(50)
    with Session(engine) as session:
        observations = session.execute(stmt).scalars().all()

    return render_template(
        "observation/home.html",
        observations=observations,
        **kwargs,
    )


@observation_bp.route("/")
def home():
    return render_home_page()


@observation_bp.route("/add", methods=["POST"])
def add_observation():
    form = request.form

    email = form.get("email")
    starname = form.get("starname")
    telname = form.get("telname")
    city = form.get("city")
    country = form.get("country")

    missing_params = []
    if not email:
        missing_params.append("Email")
    if not starname:
        missing_params.append("Star name")
    if not telname:
        missing_params.append("Telescope name")
    if not city:
        missing_params.append("City")
    if not country:
        missing_params.append("Country")

    if missing_params:
        return render_home_page(
            error=f"Invalid form input. Misisng or invalid {', '.join(missing_params)}"
        )

    # Retrieve user and telescope from DB.
    stmt_user = select(User).where(User.email == email)
    stmt_tel = select(Telescope).where(Telescope.name == telname)  # name is unique
    with Session(engine) as session:
        user = session.execute(stmt_user).scalar_one_or_none()
        telescope = session.execute(stmt_tel).scalar_one_or_none()

    if not user:
        return render_home_page(
            error=f"User email {email} is not in our database.",
            hint="add-user",
        )

    if not telescope:
        return render_home_page(
            error=f"Telescope name {telname} is not in our database.",
            hint="add-telescope",
        )

    # Get star
    star = find_existing_or_create_star(starname)  # noqa # type: ignore

    if not star:
        return render_home_page(
            error=f"Star name {starname} was not matched to any star on the SIMBAD database.",
        )

    # Add observation to the db.
    with Session(engine) as session:
        new_obs = Observation(
            user=user,
            star=star,
            telescope=telescope,
            time=datetime.now(),
            city=city,
            country=country,
        )

        try:
            session.add(new_obs)
            session.commit()

        except Exception as e:
            session.rollback()
            return render_home_page(error=f"Server error in adding observation {e}.")

    return render_home_page(success=True)
