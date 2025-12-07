from typing import Optional

from flask import Blueprint, request, jsonify
from sqlalchemy import select
from sqlalchemy.orm import Session

from models.star import Star
from models.observation import Observation
from helpers.starutils import find_existing_or_create_star
from helpers.simbad_queries import get_full_type_description
from database import engine

star_api_bp = Blueprint("api-star", __name__, url_prefix="/api/star")


@star_api_bp.route("/<starname>")
def get_star(starname: str):
    star: Optional[Star] = find_existing_or_create_star(starname)

    if not star:
        return {"error": "Star name queried does not exist on SIMBAD."}, 400

    response: dict = star.to_dict()
    response["startype_desc"] = get_full_type_description(response["startype"])

    # Limit get request to getting 50 most recent
    num_observations = min(50, request.args.get("observations", 0, type=int))

    # Get observations
    if num_observations > 0:
        stmt = (
            select(Observation)
            .where(Observation.star == star)
            .order_by(Observation.time.desc())
            .limit(num_observations)
        )
        with Session(engine) as session:
            observations = session.execute(stmt).scalars().all()

        response["observations"] = [
            obs.to_dict(exclude=["star_name", "starid"]) for obs in observations
        ]

    return jsonify(response), 200
