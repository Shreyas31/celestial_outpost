import os

from flask import Flask, render_template, request
from sqlalchemy import create_engine, select, delete
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session, joinedload

from star import star_bp
from telescope import telescope_dp
from observation import observation_dp
from user import user_bp

from datetime import date
import requests
from requests import Response

app = Flask(__name__)
app.register_blueprint(star_bp)
app.register_blueprint(telescope_bp)
app.register_blueprint(observation_bp)
app.register_blueprint(user_bp)

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

@app.route("/", methods=['GET','POST'])
def home():
    
    url: str = "https://api.nasa.gov/planetary/apod"

    today_date: dict = {
        "date": date.today().strftime("%Y-%m-%d"),
        "api_key": "DEMO_KEY"
    }

    picture_of_the_day_NASA: Response = requests.get(url, params=today_date)
    data = picture_of_the_day_NASA.json()
    image_url = picture_of_the_day_NASA["url"]

    return render_template("home.html", image_url=image_url)
    