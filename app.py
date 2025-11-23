from flask import Flask, request, render_template

from sqlalchemy import create_engine, select, delete
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session

from dotenv import load_dotenv

app = Flask(__name__)


@app.route("/")
def page_home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )
