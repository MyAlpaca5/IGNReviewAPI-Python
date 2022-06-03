import pandas as pd

from ..utils.config import get_settings
from .process_data import process_raw
from .populate_db import populate_db


def create_and_populate_db() -> None:
    """
    Read from a csv file, sanitize data, and create and populate database
    """

    cvs_path = get_settings().CSV_PATH

    # read from csv file using UTF-8 encoding
    df = pd.read_csv(cvs_path, encoding="utf8", na_values=' ')

    # sanitize the raw data
    df, data_set = process_raw(df)

    # create and populate the database
    populate_db(df, data_set)
