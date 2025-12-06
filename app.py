from flask import Flask, render_template
from datetime import date
import requests
from requests import Response

from star import star_bp
from telescope import telescope_bp
from user import user_bp

# from observation import observation_bp

app = Flask(__name__)
app.register_blueprint(star_bp)
app.register_blueprint(telescope_bp)
app.register_blueprint(user_bp)
# app.register_blueprint(observation_bp)


@app.route("/", methods=["GET", "POST"])
def home():

    url: str = "https://api.nasa.gov/planetary/apod"

    today_date: dict = {
        "date": date.today().strftime("%Y-%m-%d"),
        "api_key": "DEMO_KEY",
    }

    picture_of_the_day_NASA: Response = requests.get(url, params=today_date)
    data: dict = picture_of_the_day_NASA.json()
    image_url = data.get("url")

    return render_template("home.html", image_url)
