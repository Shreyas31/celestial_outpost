from flask import Flask, render_template

from .star import star_bp

# from sqlalchemy import create_engine, select, delete
# from sqlalchemy.engine import URL
# from sqlalchemy.orm import Session

# from dotenv import load_dotenv

app = Flask(__name__)
app.register_blueprint(star_bp)


@app.route("/")
def page_home():
    return render_template("home.html")
