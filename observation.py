from flask import Blueprint

# from models.observation import Observation
# from database import engine

observation_bp = Blueprint("observation", __name__, url_prefix="/observation")
