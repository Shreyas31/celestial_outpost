import os
from flask import Flask, Blueprint, render_template, request, redirect, url_for
from sqlalchemy import create_engine, select
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session, joinedload

telescope_bp = Blueprint("star", __name__, url_prefix="/telescope")

app = Flask(__name__)

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

from models.telescope import Telescope

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
        telescopes = session.execute(
            select(Telescope)
        ).scalars().all()
    return render_template("telescope/home.html", telescopes=telescopes)

# redirection for adding new telescope
@telescope_bp.route("/add", methods=["POST"])
def get_telescope():
    name = request.form.get("t_name")
    manufacturer = request.form.get("t_name")
    aperture = request.form.get("t_name")
    magnitude = request.form.get("t_name")
    focuslength = request.form.get("t_name")
    fieldwidth = request.form.get("t_name")
    fieldheight = request.form.get("t_name")
    length = request.form.get("t_name")
    weight = request.form.get("t_name")
    purchasable = request.form.get("t_name")
    imageurl = request.form.get("t_name")

    with Session(engine) as session:
        new_telescope = Telescope(
            name=name, 
            manufacturer=manufacturer,
            aperture=aperture, 
            magnitude=magnitude,
            focuslength=focuslength,
            fieldwidth=fieldwidth,
            fieldheight=fieldheight,
            length=length,
            weight=weight,
            purchasable=purchasable,
            imageurl=imageurl)
        
        session.add(new_telescope)
        session.commit()

        return redirect(url_for("home"))

# searching for telescope
@telescope_bp.rout("/search", method=["POST"])
def search_telescope():
    searchid = request.form.get("t_search_id")
    searchname = request.form.get("t.")