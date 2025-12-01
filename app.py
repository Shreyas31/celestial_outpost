import os

from flask import Flask, render_template, request
from sqlalchemy import create_engine, select, delete
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session, joinedload

from star import star_bp

app = Flask(__name__)
app.register_blueprint(star_bp)

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


@app.route("/")
def home():
    return render_template("home.html")
