import os

os.environ["PG_URL"] = (
    "postgresql+psycopg2://astro_query_dbastro_query:astro-queryKKO71@4.234.160.193:5432/astro_query_db?client_encoding=utf8"
)

import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_status_code(client):
    response = client.get("/")
    assert response.status_code == 200