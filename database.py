import os
from sqlalchemy import create_engine

url = os.getenv("PG_URL")

if url is None:
    raise ValueError("No URL given for Postgress DB.")

engine = create_engine(url)
