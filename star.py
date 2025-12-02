from flask import Blueprint, request, render_template, redirect, url_for
from astroquery.simbad import Simbad
from typing import Optional
from models.star import Star

import os
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select

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


print(url)

engine = create_engine(url)


@star_bp.route("/")
def home():
    return render_template("star/home.html")


def query_star_name(common_name: str) -> Optional[str]:
    """
    Given the common name of a star, queries via SIMBAD
    to find its scientific name (stored in the db).
    """
    simbad = Simbad()
    q = simbad.query_object(common_name)

    if not q:
        # Query did not return find any star
        return

    return q["main_id"][0]


@star_bp.route("/search", methods=["POST"])
def query_star():
    common_name = request.form["starname"]

    starname = query_star_name(common_name)

    if not starname:
        # TODO: Add "error message" to user for "star not found"
        return render_template("star/home.html")

    return redirect(url_for("star.detail_star", starname=starname))


@star_bp.route("/<starname>")
def detail_star(starname: str):
    with Session(engine) as session:
        stmt = select(Star).where(Star.starname == starname)
        star = session.execute(stmt).scalar_one_or_none()

        observations = star.observations if star else []

    return render_template(
        "star/detail.html",
        starname=starname,
        star=star,
        observations=observations,
    )
