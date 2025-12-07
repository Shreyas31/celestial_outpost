from flask import Blueprint, jsonify, request
from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session

# from models.star import Star
# from models.telescope import Telescope

from models.user import User
from models.observation import Observation
from database import engine

api_bp = Blueprint("api", __name__, url_prefix="/api")

# =====================
# == USER API ROUTES ==
# =====================


@api_bp.route("/user/<int:id>")
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

        response["observations"] = [obs.to_dict() for obs in observations]

    return response, 200


@api_bp.route("/user/top/<int:count>")
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

                response[i]["observations"] = [obs.to_dict() for obs in observations]

    return jsonify(response), 200


# =====================
# == STAR API ROUTES ==
# =====================


# ==========================
# == TELESCOPE API ROUTES ==
# ==========================
