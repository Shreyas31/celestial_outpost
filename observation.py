import os
from flask import Flask, Blueprint, render_template, request, redirect, url_for
from sqlalchemy import create_engine, select, desc
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session, joinedload

observation_bp = Blueprint("observation", __name__, url_prefix="/observation")

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

# home page for observation
@observation_bp.route("/",methods=["GET","POST"])
def home():
    with Session(engine) as session:
        telescopes = session.execute(
            select(Telescope).order_by(desc(Telescope.id).limit(10))
        ).scalars().all()

    if methods == 

    searchid = int(request.form.get("t_search_id"))
    searchname = request.form.get("t_search_name")

    with Session(engine) as session:
        stmt = select(Telescope).where(
            (Telescope.name == searchname) |
            (Telescope.id == searchid)
        )
        telescope = session.execute(stmt).scalar_one_or_none()

    return render_template("telescope/home.html", telescopes=telescopes, search=None, error=None)

# redirection for adding new telescope
@observation_bp.route("/add", methods=["POST"])
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
@observation_bp.route("/search", methods=["POST"])
def search_telescope():
    searchid = int(request.form.get("t_search_id"))
    searchname = request.form.get("t_search_name")
    
    with Session(engine) as session:
        stmt = select(Telescope).where(
            (Telescope.name == searchname) |
            (Telescope.id == searchid)
        )

        telescope = session.execute(stmt).scalar_one_or_none()

        if telescope:
            return redirect(f"/telescope/{telescope.id}")
        return redirect(url_for("home", error="Not found, Please enter a new telescope."))
    



