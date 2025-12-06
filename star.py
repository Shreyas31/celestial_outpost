from flask import Blueprint, request, render_template, redirect, url_for
from sqlalchemy.orm import Session
from sqlalchemy import select

from models.star import Star
from models.observation import Observation
from starutils import find_existing_or_create_star
from database import engine
from simbad_queries import (
    query_star_name,
    get_full_type_description,
)

star_bp = Blueprint("star", __name__, url_prefix="/star")


def render_home_page(**kwargs):
    stmt = select(Star).limit(25)
    with Session(engine) as session:
        stars = session.execute(stmt).scalars().all()

    return render_template(
        "star/home.html",
        stars=stars,
        **kwargs,
    )


@star_bp.route("/")
def home():
    return render_home_page()


@star_bp.route("/search", methods=["POST"])
def query_star():
    queried_name = request.form.get("f_starname", default="")

    starname = query_star_name(queried_name)

    if not starname:
        return render_home_page(error="Star queried not found on the SIMBAD database.")

    return redirect(
        url_for(
            "star.detail_star",
            starname=starname,
            queried_name=queried_name,
        )
    )


@star_bp.route("/<starname>")
def detail_star(starname: str):
    star = find_existing_or_create_star(starname)

    if not star:
        return render_home_page(error=f"Star with star name {starname} does not exist.")

    startype = get_full_type_description(star.startype)
    queried_name = request.args.get("queried_name")

    # Get recent 50 observations of this star
    stmt = (
        select(Observation)
        .where(Observation.star == star)
        .order_by(Observation.time.desc())
        .limit(50)
    )
    with Session(engine) as session:
        observations = session.execute(stmt).scalars().all()

    return render_template(
        "star/detail.html",
        star=star,
        starname=starname,
        queried_name=queried_name,
        startype=startype,
        observations=observations,
    )
