import os
from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from base import db
from user import User
from sqlalchemy import create_engine, select
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session

user_bp = Blueprint("user", __name__, url_prefix = "/user")

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
        flash("Lastname, Firstname, Email, City, and Country are required.", "error")
        return redirect(url_for(".home"))

    with Session(engine) as session:
        existing_user = session.execute(select(User).filter_by(email = email).scalar_one_or_none()
        if existing_user:
            flash("User with this email already exists.", "error")
            return redirect(url_for(".home"))

        new_user = User(
        lastname=lastname,
        firstname=firstname,
        middlenames=middlenames,
        initials=initials,
        email=email,
        institution=institution,
        city=city,
        country=country
    )

    try:
        session.add(new_user)
        session.commit()

        # Append to populate-db.sql
        sql_statement = f"INSERT INTO user (lastname, firstname, middlenames, initials, email, institution, city, country) VALUES ('{lastname}', '{firstname}', '{middlenames}', '{initials}', '{email}', '{institution}', '{city}', '{country}');\n"
        
        with open("populate-db.sql", "a") as f:
            f.write(sql_statement)

        flash("User added successfully!", "success")
    except Exception as e:
        session.rollback()
        flash(f"Error adding user: {str(e)}", "error")

    return redirect(url_for(".home"))

@user_bp.route("/search", methods = ["POST"])
def search_observer():
    email = request.form.get("search_email")
    user = None
    if email:
        with Session(engine) as session:
            user = session.execute(select(User).filter_by(email=email)).scalar_one_or_none()

    return render_template("user/home.html", search_result = user, search_email = email)

app.register_blueprint(user_bp)
