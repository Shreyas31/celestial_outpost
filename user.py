import os
from typing import Optional

from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from sqlalchemy import create_engine, select
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session

user_bp = Blueprint("user", __name__, url_prefix="/user")

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

from models.user import User


@user_bp.route("/")
def home():
    return render_template("user/home.html")


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
        return render_template(
            "user/home.html",
            error="Lastname, Firstname, Email, City, and Country are required.",
        )

    with Session(engine) as session:
        stmt = select(User).where(User.email == email)
        existing_user = session.execute(stmt).scalar_one_or_none()
        if existing_user:
            return render_template(
                "user/home.html", error="User with this email already exists."
            )

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
            return render_template(
                "user/home.html", error="Server error in adding user."
            )

        return redirect(url_for("user.detail_observer", id=new_user.id))


@user_bp.route("/search", methods=["POST"])
def search_observer_by_name():
    name = request.form.get("name")
    if not name:
        return render_template("user/home.html", error="No name given to search by.")

    with Session(engine) as session:
        stmt = select(User).where((User.lastname == name))
        users = session.execute(stmt).scalars().all()

    if not users:
        return render_template("user/home.html", error="No matching user found.")

    return render_template("user/home.html", user_list=users)


@user_bp.route("/<int:id>")
def detail_observer(id: int):
    with Session(engine) as session:
        user = session.get(User, id)

    return render_template("user/detail.html", user=user)
