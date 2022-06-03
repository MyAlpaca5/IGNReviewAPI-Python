import pytest

from app.simple_db.crud import reviewCRUD, mediatypeCRUD, publisherCRUD


@pytest.mark.parametrize(
    "id, name", [(1, "Apex Legends"), (2, "Asgard’s Wrath"), (3, "Atlas")]
)
def test_review_get_by_id(db_session, id, name):
    db_obj = reviewCRUD.read_one_by_id(db_session, id)
    assert db_obj.name == name


def test_review_get_multiple(db_session):
    offset, limit = 2, 3
    db_objs = reviewCRUD.read_range(db_session, skip=offset, limit=limit)
    for i, db_obj in enumerate(db_objs):
        assert db_obj.id == (i + offset + 1)


@pytest.mark.parametrize(
    "parameters, name",
    [
        (
            {"media_type_id": 1, "publisher_id": 6},
            "Bird Box"
        ),
        (
            {"media_type_id": 3, "posted_year": 2018, "score": 8},
            "Crash Team Racing Nitro-Fueled",
        ),
    ],
)
def test_review_get_by_parameters(db_session, parameters, name):
    db_obj = reviewCRUD.get_reviews_with_parameters(db_session, parameters)
    assert db_obj[0].name == name


@pytest.mark.parametrize("id, name", [(1, "Movie"), (2, "Show"), (3, "Game")])
def test_mediatype_get_by_id(db_session, id, name):
    db_obj = mediatypeCRUD.read_one_by_id(db_session, id)
    assert db_obj.type_name == name


def test_mediatype_get_overview(db_session):
    db_objs = mediatypeCRUD.get_overview(db_session)
    assert db_objs["items"][0][1] == "Movie"
    assert db_objs["items"][1][1] == "Show"
    assert db_objs["items"][2][1] == "Game"


@pytest.mark.parametrize(
    "id, name", [
        (1, "Oculus Studios"),
        (2, "Netflix.com"),
        (3, "Warner Home Video"),
    ]
)
def test_publisher_get_by_id(db_session, id, name):
    db_obj = publisherCRUD.read_one_by_id(db_session, id)
    assert db_obj.publisher_name == name


def test_publisher_get_overview(db_session):
    db_objs = publisherCRUD.get_overview(db_session)
    assert db_objs["items"][0][1] == "Oculus Studios"
    assert db_objs["items"][7][1] == "Shudder"
    assert db_objs["items"][12][1] == "Nintendo"
