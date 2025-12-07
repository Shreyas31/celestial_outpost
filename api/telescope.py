from flask import Blueprint, request, jsonify
from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session

from models.telescope import Telescope
from models.observation import Observation
from database import engine

telescope_api_bp = Blueprint("api-telescope", __name__, url_prefix="/api/telescope")


@telescope_api_bp.route("/<int:id>")
def get_telescope(id: int):
    with Session(engine) as session:
        telescope = session.get(Telescope, id)

    if not telescope:
        return {"error": f"No telescope of id {id}"}, 404

    response: dict = telescope.to_dict()

    # Limit get request to getting 50 most recent
    num_observations = min(50, request.args.get("observations", 0, type=int))

    # Get observations
    if num_observations > 0:
        stmt = (
            select(Observation)
            .where(Observation.telescope == telescope)
            .order_by(Observation.time.desc())
            .limit(num_observations)
        )
        with Session(engine) as session:
            observations = session.execute(stmt).scalars().all()

        response["observations"] = [
            obs.to_dict(exclude=["telescope_name", "telescopeid"])
            for obs in observations
        ]

    return response, 200


@telescope_api_bp.route("/add", methods=["POST"])
def add_telescope():
    data = request.get_json()

    if not data:
        return {"error": "No data received"}, 400

    if not isinstance(data, dict):
        return {"error": "Input should be an object"}, 400

    required_cols = (
        "name",
        "magnitude",
        "focuslength",
        "purchasable",
        "aperture",
    )

    missing_cols = []
    for col in required_cols:
        if col not in data:
            missing_cols.append(col)

    if missing_cols:
        return {"error": f"Missing columns: {', '.join(missing_cols)}"}, 400

    other_cols = (
        "manufacturer",
        "fieldwidth",
        "fieldheight",
        "length",
        "weight",
        "imageurl",
    )

    # Test to see if user already exists. Otherwise, add.
    stmt = select(Telescope).where(Telescope.name == data["name"])
    with Session(engine) as session:
        existing_telescope = session.execute(stmt).scalar_one_or_none()
        if existing_telescope:
            return {"error": "Telescope already exists in the database"}, 400

        new_telescope = Telescope()

        for col in required_cols + other_cols:
            expected_type = Telescope.__table__.columns[col].type.python_type

            if col in data and not isinstance(data[col], expected_type):
                return {
                    "error": f"Type of argument '{col}' is incorrect: expected {expected_type}."
                }, 400
            setattr(new_telescope, col, data.get(col))

        try:
            session.add(new_telescope)
            session.commit()
            id = new_telescope.id

        except Exception as e:
            session.rollback()
            print(e)
            return {"error": f"Server error in adding telescope"}, 500

    return {
        "success": "Successfully added telescope to the database",
        "telescopeid": id,
    }, 200
