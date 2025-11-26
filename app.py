import os

from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, select, delete
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session, joinedload
from flask import Flask, render_template

from .star import star_bp

# from sqlalchemy import create_engine, select, delete
# from sqlalchemy.engine import URL
# from sqlalchemy.orm import Session

# from dotenv import load_dotenv

app = Flask(__name__)
app.register_blueprint(star_bp)

url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    query={"client_encoding": "utf8"}
)

engine = create_engine(url)

@app.route("/")
def page_home():
    return render_template("home.html")
