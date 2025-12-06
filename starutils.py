from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.star import Star
from simbad_queries import query_star_name, query_star_details
from database import engine


def find_existing_or_create_star(common_name: str) -> Optional[Star]:
    """
    Given the common name of a star, will:
      - If the star's name does not exist, will return None.
      - If the star already exists in the db, will return the star's ID.
      - If the star doesn't exist in the db, will create it, and
        return the star's ID.

    This should be used by observation.py whenever a new observation
    is created for a star that does not exist, or to bind it to an
    existing star.
    """
    starname: Optional[str] = query_star_name(common_name)

    # Star's name cannot be found
    if not starname:
        return None

    with Session(engine) as session:
        stmt = select(Star).where(Star.starname == starname)
        star = session.execute(stmt).scalar_one_or_none()

        # Create star if it does not exist:
        if not star:
            details = query_star_details(starname)

            star = Star(
                starname=starname,
                startype=details["otype"],
                coordra=details["ra"],
                coorddec=details["dec"],
                color=details["sp_type"],
                appmagnitude=details["app_mag"],
                measurefilter=details["filter"],
            )
            try:
                session.add(star)
                session.commit()

            except Exception:
                session.rollback()
                return None

    return star
