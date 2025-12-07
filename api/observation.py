from flask import Blueprint

observation_api_bp = Blueprint(
    "api-observation", __name__, url_prefix="/api/observation"
)
