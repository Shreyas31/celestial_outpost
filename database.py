import os
from sqlalchemy import create_engine
# from sqlalchemy.engine import URL

# url = URL.create(
#     drivername="postgresql+psycopg2",
#     username=os.getenv("DB_USER"),
#     password=os.getenv("DB_PASSWORD"),
#     host=os.getenv("DB_HOST"),
#     port=int(os.getenv("DB_PORT")),  # type: ignore  # noqa
#     database=os.getenv("DB_NAME"),
#     query={"client_encoding": "utf8"},
# )

url = os.getenv("PG_URL")

if url is None:
    raise ValueError("No URL given for Postgress DB.")

engine = create_engine(url)
