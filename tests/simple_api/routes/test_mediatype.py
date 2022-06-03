import pytest


@pytest.mark.parametrize(
    "id, name", [(1, "Movie"), (2, "Show"), (3, "Game")]
)
def test_mediatype_id(api_client, id, name):
    response = api_client.get(f"/mediatype/{id}")
    assert response.status_code == 200
    assert response.json()["type_name"] == name


def test_mediatype_id_failure(api_client):
    response = api_client.get("/mediatype/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Media Type not found given id = 999"


def test_publisher_overview(api_client):
    response = api_client.get("/mediatype")
    assert response.status_code == 200
    publishers = response.json()
    assert publishers["size"] == 3
    assert publishers["items"][0][1] == "Movie"
    assert publishers["items"][1][1] == "Show"
    assert publishers["items"][2][1] == "Game"
