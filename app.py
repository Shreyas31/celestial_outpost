import requests
from requests import Response
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Optional

from flask import Flask, render_template

from web.star import star_bp
from web.telescope import telescope_bp
from web.user import user_bp
from web.observation import observation_bp

from api.star import star_api_bp
from api.telescope import telescope_api_bp
from api.user import user_api_bp
from api.observation import observation_api_bp

app = Flask(__name__)

app.register_blueprint(star_bp)
app.register_blueprint(telescope_bp)
app.register_blueprint(user_bp)
app.register_blueprint(observation_bp)

app.register_blueprint(star_api_bp)
app.register_blueprint(telescope_api_bp)
app.register_blueprint(user_api_bp)
app.register_blueprint(observation_api_bp)


@app.route("/", methods=["GET", "POST"])
def home():
    url: str = "https://api.nasa.gov/planetary/apod"
    API_KEY = "wEBGgaS95dGL6qtXFfHE6q4ViVALH7DIE48lJbNb"

    NY_TZ = ZoneInfo("America/New_York")
    current_date = datetime.now(NY_TZ)

    data: dict = {}
    media_type: Optional[str] = None

    while media_type != "image":

        date_param: str = current_date.strftime("%Y-%m-%d")

        today_date_params: dict = {
            "date": date_param,
            "api_key": API_KEY,
        }

        picture_of_the_day_NASA: Response = requests.get(url, params=today_date_params)
        data = picture_of_the_day_NASA.json()

        media_type: Optional[str] = data.get("media_type")

        if media_type != "image":
            current_date = current_date - timedelta(days=1)

    image_url: Optional[str] = data.get("url")

    return render_template(
        "home.html",
        image_url=image_url,
        media_type=media_type
    )