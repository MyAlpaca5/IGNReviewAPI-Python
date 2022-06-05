import json
from fastapi import Depends, HTTPException, FastAPI
from sqlalchemy.orm import Session

from .cache import LFUCache
from .data_schemas import (
    PublisherOverview,
    MediaTypeOverview,
    ReviewForMediaType,
    ReviewForPublisher,
    ReviewBase,
)
from ..simple_db import crud
from ..simple_db.database import create_session_generator, Base


app = FastAPI(
    title="CodeFoo Intern Application Demo",
    version="0.1",
    contact={
        "name": "Pinhao Guo",
        "email": "pinhaog2@illinois.edu",
    },
    redoc_url=None,
)
cache = LFUCache[str, Base](capacity=50)


@app.get("/reviews/{id}", response_model=ReviewBase)
def get_review_by_id(id: int, db: Session = Depends(create_session_generator)):
    search_str = "review" + str(id)
    db_obj = cache.get(search_str)
    if db_obj is None:
        db_obj = crud.reviewCRUD.read_one_by_id(db, id)
        cache.put(search_str, db_obj)

    if db_obj is None:
        raise HTTPException(status_code=404, detail=f"Review not found given id = {id}")

    return db_obj


@app.get("/reviews/", response_model=list[ReviewBase])
def get_reviews_by_parameter(
    db: Session = Depends(create_session_generator),
    media_type_id: int | None = None,
    publisher_id: int | None = None,
    posted_year: int | None = None,
    score: float | None = None,
):

    # build the paramter filter
    # TODO: following solution doesn't scale well, need better approach
    parameters = {}
    if media_type_id is not None:
        parameters["media_type_id"] = media_type_id
    if publisher_id is not None:
        parameters["publisher_id"] = publisher_id
    if posted_year is not None:
        parameters["posted_year"] = posted_year
    if score is not None:
        parameters["score"] = score

    search_str = json.dumps(parameters)
    db_obj = cache.get(search_str)
    if db_obj is None:
        db_obj = crud.reviewCRUD.get_reviews_with_parameters(db, parameters)
        cache.put(search_str, db_obj)

    if db_obj is None:
        raise HTTPException(
            status_code=404, detail=f"Review not found given parameters"
        )
    return db_obj


@app.get("/mediatype/", response_model=MediaTypeOverview)
def get_mediatype_overview(db: Session = Depends(create_session_generator)):
    search_str = "mediatypeoverview"
    db_obj = cache.get(search_str)
    if db_obj is None:
        db_obj = crud.mediatypeCRUD.get_overview(db)
        cache.put(search_str, db_obj)

    return db_obj


@app.get("/mediatype/{id}", response_model=ReviewForMediaType)
def get_mediatype_by_id(id: int, db: Session = Depends(create_session_generator)):
    search_str = "mediatype" + str(id)
    db_obj = cache.get(search_str)
    if db_obj is None:
        db_obj = crud.mediatypeCRUD.read_one_by_id(db, id)
        cache.put(search_str, db_obj)

    if db_obj is None:
        raise HTTPException(
            status_code=404, detail=f"Media Type not found given id = {id}"
        )
    return db_obj


@app.get("/publisher/", response_model=PublisherOverview)
def get_publisher_overview(db: Session = Depends(create_session_generator)):
    search_str = "publisheroverview"
    db_obj = cache.get(search_str)
    if db_obj is None:
        db_obj = crud.publisherCRUD.get_overview(db)
        cache.put(search_str, db_obj)

    return db_obj


@app.get("/publisher/{id}", response_model=ReviewForPublisher)
def get_publisher_by_id(id: int, db: Session = Depends(create_session_generator)):
    search_str = "publisher" + str(id)
    db_obj = cache.get(search_str)
    if db_obj is None:
        db_obj = crud.publisherCRUD.read_one_by_id(db, id)
        cache.put(search_str, db_obj)

    if db_obj is None:
        raise HTTPException(
            status_code=404, detail=f"Publisher not found given id = {id}"
        )
    return db_obj


# Could add more route for creator, gener, etc.
# But for simplicity, currently only implemented three routes above
