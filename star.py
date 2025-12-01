from flask import Blueprint, request, render_template, redirect, url_for
from astroquery.simbad import Simbad
from typing import Optional

star_bp = Blueprint("star", __name__, url_prefix="/star")

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
    # TODO: Query DB and get relevant information to display. If star is not
    # in DB, lead to a page where that can be shown, and an "add observation"
    # option is given.

    # TODO: Adjust star/detail.html to show the relevant information.

    return render_template("star/detail.html")
