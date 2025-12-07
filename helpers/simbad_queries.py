import csv
from typing import Optional, Any

from numpy import floating
from astroquery.simbad import Simbad


### OBJECT TYPES
otype_to_label: dict[str, str] = {}
label_to_desc: dict[str, str] = {}
label_to_img: dict[str, str] = {}

with open("helpers/object_types.csv", "r") as f:
    f.readline()  # Remove headers

    reader = csv.reader(f)

    for line in reader:
        key, label, desc, img_url = line
        otype_to_label[key] = label
        label_to_desc[label] = desc
        label_to_img[label] = img_url


### SIMBAD QUERIES
def query_star_name(common_name: str) -> Optional[str]:
    """
    Given the common name of a star, queries via SIMBAD to find
    its scientific name. If the query does not match any object,
    will return None.
    """
    simbad = Simbad()
    q = simbad.query_object(common_name)

    if not q:
        # Query did not return find any star
        return None

    return q["main_id"][0]


def query_star_details(object_name: str) -> dict[str, Any]:
    """
    Given the name of an object, returns its details as a dict of
    strings. Currently, this includes:
      - `main_id`: name (designation).
      - `ra`: Right Ascension.
      - `dec`: Declination.
      - `sp_type`: Spectral type (color).
      - `otype`: Object type.
      - `app_mag`: Apparent magnitude of star at measured filter.
      - `filter`: Filter used for apparent magnitude measurement.

    If the query does not match any SIMBAD object, throws a ValueError.
    query_star_name() can be used first to check whether the object exsits.
    """
    simbad = Simbad()
    simbad.add_votable_fields("sp_type", "allfluxes", "otype")
    q = simbad.query_object(object_name)

    star_data: dict[str, Any] = {}

    if not q:
        raise ValueError(f"{object_name} does not match any query on Simbad.")

    # Add the simple headers:
    simple_headers = ("main_id", "ra", "dec", "sp_type")
    for head in simple_headers:
        star_data[head] = q[head][0]

    # Add object type:
    star_data["otype"] = otype_to_label.get(q["otype"][0], "Unknown")

    # Query for fluxes:
    star_data["app_mag"] = ""
    star_data["filter"] = ""

    # Order in which to check for existing magnitude measurements.
    for filter in ("V", "G", "g", "r", "B", "R", "i", "I"):
        if q[filter][0]:
            star_data["app_mag"] = q[filter][0]
            star_data["filter"] = filter
            break

    # Cast numpy values to float
    for k, v in star_data.items():
        if isinstance(v, floating):
            star_data[k] = float(v)

    return star_data


# HELPER FUNCTIONS
def get_full_type_description(object_type: Optional[str]) -> Optional[str]:
    if object_type is None:
        return None

    return label_to_desc.get(object_type)


def get_image_url(object_type: Optional[str]) -> str:
    if object_type is None:
        return "unknown.png"

    return label_to_img.get(object_type, "unknown.png")
