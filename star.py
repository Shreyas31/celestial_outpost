import os
from typing import Optional

from flask import Blueprint, request, render_template, redirect, url_for
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select

from models.star import Star
from simbad_queries import (
    query_star_name,
    query_star_details,
    get_full_type_description,
)


star_bp = Blueprint("star", __name__, url_prefix="/star")

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


@star_bp.route("/")
def home():
    return render_template("star/home.html")


@star_bp.route("/search", methods=["POST"])
def query_star():
    queried_name = request.form.get("f_starname", default="")

    starname = query_star_name(queried_name)

    if not starname:
        # TODO: Add "error message" to user for "star not found"
        return render_template("star/home.html")

    return redirect(
        url_for(
            "star.detail_star",
            starname=starname,
            queried_name=queried_name,
        )
    )


@star_bp.route("/<starname>")
def detail_star(starname: str):
    with Session(engine) as session:
        stmt = select(Star).where(Star.starname == starname)
        star = session.execute(stmt).scalar_one_or_none()

        observations = star.observations if star else []
        startype = get_full_type_description(star.startype) if star else None

    queried_name = request.args.get("queried_name")

    return render_template(
        "star/detail.html",
        starname=starname,
        queried_name=queried_name,
        star=star,
        startype=startype,
        observations=observations,
    )


def find_existing_or_create_star(common_name: str) -> Optional[int]:
    """
    Given the common name of a star, will:
      - If the star's name does not exist, will return None.
      - If the star already exists in the db, will return the star's ID.
      - If the star doesn't exist in the db, will create it, and
        return the star's ID.

    This should be used by observation.py whenever a new observation
    is created for a star that does not exist, or to bind it to an
    existing star.
    """
    starname: Optional[str] = query_star_name(common_name)

    # Star's name cannot be found
    if not starname:
        return None

    with Session(engine) as session:
        stmt = select(Star).where(Star.starname == starname)
        star = session.execute(stmt).scalar_one_or_none()

        # Create star if it does not exist:
        if not star:
            details = query_star_details(starname)

            star = Star(
                starname=starname,
                startype=details["otype"],
                coordra=details["ra"],
                coorddec=details["dec"],
                color=details["sp_type"],
                appmagnitude=details["app_mag"],
                measurefilter=details["filter"],
            )
            try:
                session.add(star)
                session.commit()

            except Exception as e:
                session.rollback()

    return star.id
