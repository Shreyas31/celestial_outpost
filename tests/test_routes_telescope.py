import pytest

from app import app


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


# Search telescope - search not matching
def test_search_telescope_error(client):
    form_data = {
        "f_search_id": "-1",
        "f_search_name": "NonExistingScopeName",
    }
    response = client.post("/telescope/search", data=form_data)
    assert response.status_code == 200
    assert b"Telescope queried not found." in response.data
