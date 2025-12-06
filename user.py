from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session

from models.user import User
from models.observation import Observation
from database import engine

user_bp = Blueprint("user", __name__, url_prefix="/user")


def render_home_page(**kwargs):
    # Get top 50 users and their number of observations
    stmt = (
        select(User, func.count(Observation.id).label("obs_count"))
        .join(Observation)
        .group_by(User.id)
        .order_by(desc("obs_count"))
        .limit(50)
    )

    with Session(engine) as session:
        results = session.execute(stmt).all()

    users: list[User] = []
    counts: list[int] = []

    for u, c in results:
        users.append(u)
        counts.append(c)

    # Get the most recent 5 observations for each user
    observed_stars = []
    with Session(engine) as session:
        for user in users:
            stmt = (
                select(Observation)
                .where(Observation.user == user)
                .order_by(Observation.time.desc())
                .limit(5)
            )
            user_obs = session.execute(stmt).scalars().all()

            observed_stars.append([obs.star for obs in user_obs])

    return render_template(
        "user/home.html",
        users=users,
        counts=counts,
        observed_stars=observed_stars,
        **kwargs,
    )


@user_bp.route("/")
def home():
    return render_home_page()


@user_bp.route("/add", methods=["POST"])
def add_observer():
    lastname = request.form.get("lastname")
    firstname = request.form.get("firstname")
    middlenames = request.form.get("middlenames")
    initials = request.form.get("initials")
    email = request.form.get("email")
    institution = request.form.get("institution")
    city = request.form.get("city")
    country = request.form.get("country")

    if not lastname or not firstname or not email or not city or not country:
        return render_home_page(
            error="Lastname, Firstname, Email, City, and Country are required.",
        )

    with Session(engine) as session:
        stmt = select(User).where(User.email == email)
        existing_user = session.execute(stmt).scalar_one_or_none()
        if existing_user:
            return render_home_page(error="User with this email already exists.")

        new_user = User(
            lastname=lastname,
            firstname=firstname,
            middlenames=middlenames,
            initials=initials,
            email=email,
            institution=institution,
            city=city,
            country=country,
        )

        try:
            session.add(new_user)
            session.commit()

        except Exception as e:
            session.rollback()
            return render_home_page(error=f"Server error in adding user {e}.")

        return redirect(url_for("user.detail_observer", id=new_user.id))


@user_bp.route("/search", methods=["POST"])
def search_observer_by_name():
    name = request.form.get("name")
    if not name:
        return render_home_page(error="No name given to search by.")

    with Session(engine) as session:
        stmt = select(User).where((User.lastname == name))
        users = session.execute(stmt).scalars().all()

    if not users:
        return render_home_page(error="No matching user found.")

    return render_template("user/home.html", user_list=users)


@user_bp.route("/<int:id>")
def detail_observer(id: int):
    with Session(engine) as session:
        user = session.get(User, id)

    return render_template("user/detail.html", user=user)
