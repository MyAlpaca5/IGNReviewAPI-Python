import pytest


@pytest.mark.parametrize(
    "id, name", [(1, "Oculus Studios"), (2, "Netflix.com"), (3, "Warner Home Video")]
)
def test_publisher_id(api_client, id, name):
    response = api_client.get(f"/publisher/{id}")
    assert response.status_code == 200
    assert response.json()["publisher_name"] == name


def test_publisher_id_failure(api_client):
    response = api_client.get("/publisher/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Publisher not found given id = 999"


def test_publisher_overview(api_client):
    response = api_client.get("/publisher")
    assert response.status_code == 200
    publishers = response.json()
    assert publishers["size"] == 13
    assert publishers["items"][0][1] == "Oculus Studios"
    assert publishers["items"][7][1] == "Shudder"
    assert publishers["items"][12][1] == "Nintendo"
