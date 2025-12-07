import requests
from requests import Response
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional

from flask import Flask, render_template

from web.star import star_bp
from web.telescope import telescope_bp
from web.user import user_bp
from web.observation import observation_bp
from api.api import api_bp

app = Flask(__name__)
app.register_blueprint(star_bp)
app.register_blueprint(telescope_bp)
app.register_blueprint(user_bp)
app.register_blueprint(observation_bp)
app.register_blueprint(api_bp)


@app.route("/", methods=["GET", "POST"])
def home():
    url: str = "https://api.nasa.gov/planetary/apod"

    NY_TZ = ZoneInfo("America/New_York")

    today_date: dict = {
        "date": datetime.now(NY_TZ).strftime("%Y-%m-%d"),
        "api_key": "wEBGgaS95dGL6qtXFfHE6q4ViVALH7DIE48lJbNb",
    }

    picture_of_the_day_NASA: Response = requests.get(url, params=today_date)
    data: dict = picture_of_the_day_NASA.json()
    image_url: Optional[str] = data.get("url")

    return render_template("home.html", image_url=image_url)
