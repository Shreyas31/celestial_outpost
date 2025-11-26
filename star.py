from flask import Blueprint, render_template

star_bp = Blueprint("star", __name__, url_prefix="/star")


@star_bp.route("/")
def star_home():
    return render_template("star.html")
