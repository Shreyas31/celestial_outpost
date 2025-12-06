from flask import Blueprint, request, render_template, redirect, url_for
from sqlalchemy.orm import Session
from sqlalchemy import select

from models.star import Star
from database import engine
from simbad_queries import (
    query_star_name,
    get_full_type_description,
)


star_bp = Blueprint("star", __name__, url_prefix="/star")


@star_bp.route("/")
def home():
    return render_template("star/home.html")


@star_bp.route("/search", methods=["POST"])
def query_star():
    queried_name = request.form.get("f_starname", default="")

    starname = query_star_name(queried_name)

    if not starname:
        return render_template(
            "star/home.html", error="Star queried not found on the SIMBAD database."
        )

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
