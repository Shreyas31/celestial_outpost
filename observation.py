from flask import Blueprint, render_template, request

from models.observation import Observation
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import engine

observation_bp = Blueprint("observation", __name__, url_prefix="/observation")


@observation_bp.route("/")
def home():
    # CURRENTLY TEMPLATE DOES NOT WORK.
    return render_template("observation/home.html")


@observation_bp.route("/<int:id>")
def detail_observation(id: int):
    # THIS TEMPLATE SHOULD WORK.
    with Session(engine) as session:
        observation = session.get(Observation, id)

        if not observation:
            return render_template("observation/detail.html")

        return render_template(
            "observation/detail.html",
            observation=observation,
            user=observation.user,
            telescope=observation.telescope,
            star=observation.star,
        )
