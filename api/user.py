from flask import Blueprint, jsonify, request
from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session
from email_validator import validate_email, EmailNotValidError

from models.user import User
from models.observation import Observation
from database import engine

user_api_bp = Blueprint("api-user", __name__, url_prefix="/api/user")


def is_valid_email(email: str) -> bool:
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False


@user_api_bp.route("/<int:id>")
def get_user(id: int):
    with Session(engine) as session:
        user = session.get(User, id)

    if not user:
        return {"error": f"No user of id {id}"}, 404

    response: dict = user.to_dict()

    # Limit get request to getting 50 most recent
    num_observations = min(50, request.args.get("observations", 0, type=int))

    # Get observations
    if num_observations > 0:
        stmt = (
            select(Observation)
            .where(Observation.user == user)
            .order_by(Observation.time.desc())
            .limit(num_observations)
        )
        with Session(engine) as session:
            observations = session.execute(stmt).scalars().all()

        response["observations"] = [
            obs.to_dict(exclude=["user_name", "userid"]) for obs in observations
        ]

    return response, 200


@user_api_bp.route("/top/<int:count>")
def get_top_users(count: int):
    response: list[dict] = []

    # Limit count to 50:
    count = min(50, count)

    if count <= 0:
        return {"error": f"Count cannot be negative: {count}"}, 400

    stmt = (
        select(User, func.count(Observation.id).label("obs_count"))
        .join(Observation)
        .group_by(User.id)
        .order_by(desc("obs_count"))
        .limit(count)
    )

    with Session(engine) as session:
        results = session.execute(stmt).all()
    users: list[User] = []
    for u, c in results:
        users.append(u)
        user_dict: dict = u.to_dict()
        user_dict["obs_count"] = c

        response.append(user_dict)

    # Limit get request to getting 50 most recent
    num_observations = min(50, request.args.get("observations", 0, type=int))

    # Get observations
    if num_observations > 0:
        with Session(engine) as session:
            for i, user in enumerate(users):
                stmt = (
                    select(Observation)
                    .where(Observation.user == user)
                    .order_by(Observation.time.desc())
                    .limit(num_observations)
                )
                observations = session.execute(stmt).scalars().all()

                response[i]["observations"] = [
                    obs.to_dict(exclude=["user_name", "userid"]) for obs in observations
                ]

    return jsonify(response), 200


@user_api_bp.route("/lastname/<lastname>")
def get_users_by_lastname(lastname: str):
    with Session(engine) as session:
        stmt = select(User).where(User.lastname == lastname)
        users = session.execute(stmt).scalars().all()

    response: list[dict] = [u.to_dict() for u in users]

    # Limit get request to getting 50 most recent
    num_observations = min(50, request.args.get("observations", 0, type=int))

    # Get observations
    if num_observations > 0:
        with Session(engine) as session:
            for i, user in enumerate(users):
                stmt = (
                    select(Observation)
                    .where(Observation.user == user)
                    .order_by(Observation.time.desc())
                    .limit(num_observations)
                )
                observations = session.execute(stmt).scalars().all()

                response[i]["observations"] = [
                    obs.to_dict(exclude=["user_name", "userid"]) for obs in observations
                ]

    return jsonify(response), 200


@user_api_bp.route("/add", methods=["POST"])
def add_user():
    data = request.get_json()

    if not data:
        return {"error": "No data received"}, 400

    if not isinstance(data, dict):
        return {"error": "Input should be an object"}, 400

    required_cols = (
        "email",
        "firstname",
        "lastname",
        "city",
        "country",
    )

    missing_cols = []
    for col in required_cols:
        if col not in data:
            missing_cols.append(col)

    if missing_cols:
        return {"error": f"Missing columns: {', '.join(missing_cols)}"}, 400

    if not is_valid_email(data["email"]):
        return {"error": "Email given is not valid"}, 400

    other_cols = (
        "middlenames",
        "initials",
        "institution",
    )

    # Test to see if user already exists. Otherwise, add.
    stmt = select(User).where(User.email == data["email"])
    with Session(engine) as session:
        existing_user = session.execute(stmt).scalar_one_or_none()
        if existing_user:
            return {"error": "Email given already exists in the database"}, 400

        new_user = User()

        for col in required_cols + other_cols:
            expected_type = User.__table__.columns[col].type.python_type

            if col in data and not isinstance(data[col], expected_type):
                return {
                    "error": f"Type of argument '{col}' is incorrect: expected {expected_type}."
                }, 400
            setattr(new_user, col, data.get(col))

        try:
            session.add(new_user)
            session.commit()
            id = new_user.id

        except Exception as e:
            session.rollback()
            return {"error": "Server error in adding user"}, 500

    return {
        "success": "Successfully added user to the database",
        "id": id,
    }, 200
