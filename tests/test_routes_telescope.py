import os

os.environ["PG_URL"] = (
    "postgresql+psycopg2://astro_query_dbastro_query:astro-queryKKO71@4.234.160.193:5432/astro_query_db?client_encoding=utf8"
)

import pytest

from app import app
from database import engine
from sqlalchemy.orm import Session

from models.telescope import Telescope
from models.observation import Observation

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# Home page
def test_telescope_home_ok(client):
    response = client.get("/telescope/")
    assert response.status_code == 200

# Add telescope - wrong data
def test_add_telescope_missing_fields_shows_error(client):
    response = client.post("/telescope/add", data={})
    assert response.status_code == 200
    assert b"Invalid form input. Missing or invalid:" in response.data

# Add telescope - dup data
def test_add_telescope_duplicate_name_shows_error(client):
    existing = create_telescope(name="DuplicateScope")
    form_data = {
        "f_name": "DuplicateScope",
        "f_magnitude": "10",
        "f_focuslength": "500",
        "f_aperture": "100",
        "f_purchasable": "on",
    }
    response = client.post("/telescope/add", data=form_data)
    assert response.status_code == 200
    assert b"Telescope already exists in telescope." in response.data

# Search telescope - search not matching
def test_search_telescope_error(client):
    form_data = {
        "f_search_id": "-1",
        "f_search_name": "NonExistingScopeName",
    }
    response = client.post("/telescope/search", data=form_data)
    assert response.status_code == 200
    assert b"Telescope queried not found." in response.data