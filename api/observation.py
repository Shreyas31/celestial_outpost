from flask import Blueprint

from flask import Blueprint, request, jsonify
from sqlalchemy import select
from sqlalchemy.orm import Session

from models.star import Star
from models.telescope import Telescope
from models.user import User
from models.observation import Observation
from database import engine
from helpers.starutils import find_existing_or_create_star


observation_api_bp = Blueprint(
    "api-observation", __name__, url_prefix="/api/observation"
)


@observation_api_bp.route("/<int:id>")
def get_observation(id: int):
    """
    API endpoint to get an observation from the db.

    Params:
      - id: Observation primary key (id)
    """
    with Session(engine) as session:
        observation = session.get(Observation, id)

    if not observation:
        return {"error": f"No observation of id {id}"}, 404

    response: dict = observation.to_dict()

    return response, 200


@observation_api_bp.route("/newest/<int:count>")
def get_newest_observations(count: int):
    """
    API endpoint to get most recent observations from the db.

    Params:
      - count: Number of observations to read from the db. Max 100.
    """
    count = min(100, count)

    if count < 0:
        return {"error": "Negative count specified"}, 400

    stmt = select(Observation).order_by(Observation.time.desc()).limit(count)
    with Session(engine) as session:
        observations = session.execute(stmt).scalars().all()

    return jsonify([obs.to_dict() for obs in observations]), 200


@observation_api_bp.route("/")
def get_all_observations():
    """
    API endpoint to get all observations from the db.

    """
    stmt = select(Observation).order_by(Observation.time.desc())
    with Session(engine) as session:
        observations = session.execute(stmt).scalars().all()

    return jsonify([obs.to_dict() for obs in observations]), 200


@observation_api_bp.route("/", methods=["POST"])
def add_observation():
    """
    API endpoint to add an observation to the db. A user,
    star, telescope, city, and country must be provided.

    User can be provided either by email or primary key.
    Primary key takes precedence if both are provided.

    Star can be provided as the name or primary key.
    Primary key takes precedence if both are provided.

    Telescope can be provided by name or primary key.
    Primary key takes precedence if both are provided.

    City and country are passed as strings.
    """
    data = request.get_json()

    if not data:
        return {"error": "No data received"}, 400

    if not isinstance(data, dict):
        return {"error": "Input should be an object"}, 400

    userid = data.get("userid")
    user_email = data.get("user_email")
    starid = data.get("starid")
    star_name = data.get("star_name")
    telescopeid = data.get("telescopeid")
    telescope_name = data.get("telescope_name")
    city = data.get("city")
    country = data.get("country")

    missing_params: list[str] = []
    if userid is None and user_email is None:
        missing_params.append("userid or user_email")

    if starid is None and star_name is None:
        missing_params.append("starid or star_name")

    if telescopeid is None and telescope_name is None:
        missing_params.append("telescopeid or telescope_name")

    if city is None:
        missing_params.append("city")

    if country is None:
        missing_params.append("country")

    if missing_params:
        return {"error": f"Missing parameters: {', '.join(missing_params)}"}, 400

    # Validate input types:
    incorrect_types: list[str] = []
    if userid is not None and not isinstance(userid, int):
        incorrect_types.append("userid")
    if user_email is not None and not isinstance(user_email, str):
        incorrect_types.append("user_email")
    if starid is not None and not isinstance(starid, int):
        incorrect_types.append("starid")
    if star_name is not None and not isinstance(star_name, str):
        incorrect_types.append("star_name")
    if telescopeid is not None and not isinstance(telescopeid, int):
        incorrect_types.append("telescopeid")
    if telescope_name is not None and not isinstance(telescope_name, str):
        incorrect_types.append("telescope_name")
    if not isinstance(city, str):
        incorrect_types.append("city")
    if not isinstance(country, str):
        incorrect_types.append("country")
    if incorrect_types:
        return {"error": f"Incorrect types: {', '.join(incorrect_types)}"}, 400

    # Get corresponding user, star, and telescope:
    with Session(engine) as session:
        if userid is not None:
            user = session.get(User, userid)
        else:
            stmt = select(User).where(User.email == user_email)
            user = session.execute(stmt).scalar_one_or_none()

        if starid is not None:
            star = session.get(Star, starid)
        else:
            star = find_existing_or_create_star(star_name)  # noqa # type: ignore

        if telescopeid is not None:
            telescope = session.get(Telescope, telescopeid)
        else:
            stmt = select(Telescope).where(Telescope.name == telescope_name)
            telescope = session.execute(stmt).scalar_one_or_none()

        # Check that objects have been retrieved
        if not user:
            return {"error": "User not found"}, 400
        if not star:
            return {"error": "Star not found"}, 400
        if not telescope:
            return {"error": "Telescope not found"}, 400

        # Add observation object
        observation = Observation(
            user=user,
            star=star,
            telescope=telescope,
            city=city,
            country=country,
        )

        try:
            session.add(observation)
            session.commit()
            id = observation.id

        except Exception as e:
            session.rollback()
            return {"error": "Server error in adding observation"}, 500

    return {
        "success": "Successfully added observation to the database",
        "observationid": id,
    }, 200
