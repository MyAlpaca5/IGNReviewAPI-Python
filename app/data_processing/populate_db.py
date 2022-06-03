from typing import Dict, MutableSet
import pandas as pd
from dateutil import parser as datetimeparser
from pytz import timezone

from ..simple_db import crud, database
from ..utils.config import get_settings


def populate_db(df: pd.DataFrame, data_set: Dict[str, MutableSet]) -> None:
    """
    Create and populate database

    Parameters:
        df (pd.DataFrame): processed dataframe
        data_set (Dict[str, MutableSet]): a dictionary of set of unique element in some columns
                                          required for creating anxiliary tables

    Returns:
        None
    """

    with database.create_session() as db:
        # populate auxiliary tables first
        # also cache the db_obj to use them later when creating Review record
        if "media_types" in data_set:
            media_type_db_obj = {}
            for media_type in data_set["media_types"]:
                pair = {"type_name": media_type}
                media_type_db_obj[media_type] = crud.mediatypeCRUD.create(db, pair)
        print("populated media_type table")

        if "genres" in data_set:
            genres_db_obj = {}
            for genre in data_set["genres"]:
                pair = {"genre_name": genre}
                genres_db_obj[genre] = crud.genreCRUD.create(db, pair)
        print("populated genre table")

        if "creators" in data_set:
            creator_db_obj = {}
            for creator in data_set["creators"]:
                pair = {"creator_name": creator}
                creator_db_obj[creator] = crud.creatorCRUD.create(db, pair)
        print("populated creator table")

        if "publishers" in data_set:
            publisher_db_obj = {}
            for publisher in data_set["publishers"]:
                pair = {"publisher_name": publisher}
                publisher_db_obj[publisher] = crud.publisherCRUD.create(db, pair)
        print("populated publisher table")

        if "franchises" in data_set:
            franchise_db_obj = {}
            for franchise in data_set["franchises"]:
                pair = {"franchise_name": franchise}
                franchise_db_obj[franchise] = crud.franchiseCRUD.create(db, pair)
        print("populated franchise table")

        if "regions" in data_set:
            region_db_obj = {}
            for region in data_set["regions"]:
                pair = {"region_name": region}
                region_db_obj[region] = crud.regionCRUD.create(db, pair)
        print("populated region table")

        # populate Review Table
        for row in df.itertuples(index=False):
            pair = {}
            pair["id"] = row.id
            pair["media_type_id"] = media_type_db_obj[row.media_type].id
            pair["name"] = row.name
            pair["short_name"] = row.short_name
            pair["long_description"] = row.long_description
            pair["short_description"] = row.short_description
            created_at = datetimeparser.parse(row.created_at).astimezone(
                timezone(get_settings().TIMEZONE)
            )
            pair["created_at"] = created_at
            pair["created_year"] = created_at.year
            pair["updated_at"] = datetimeparser.parse(row.updated_at).astimezone(
                timezone(get_settings().TIMEZONE)
            )
            pair["review_url"] = row.review_url
            pair["review_score"] = row.review_score
            pair["slug"] = row.slug

            pair["genres"] = []
            for genre in row.genres_n.split(","):
                if genre == "":
                    continue
                pair["genres"].append(genres_db_obj[genre])

            pair["creators"] = []
            for creator in row.creators_n.split(","):
                if creator == "":
                    continue
                pair["creators"].append(creator_db_obj[creator])

            pair["publishers"] = []
            for publisher in row.publishers_n.split(","):
                if publisher == "":
                    continue
                pair["publishers"].append(publisher_db_obj[publisher])

            pair["franchises"] = []
            for franchise in row.franchises_n.split(","):
                if franchise == "":
                    continue
                pair["franchises"].append(franchise_db_obj[franchise])

            pair["regions"] = []
            for region in row.regions_n.split(","):
                if region == "":
                    continue
                pair["regions"].append(region_db_obj[region.strip()])

            crud.reviewCRUD.create(db, pair)
        print("populated review table")
