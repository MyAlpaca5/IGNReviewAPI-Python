import pytest


@pytest.mark.parametrize(
    "id, name", [(1, "Apex Legends"), (2, "Asgard’s Wrath"), (3, "Atlas")]
)
def test_review_id(api_client, id, name):
    response = api_client.get(f"/reviews/{id}")
    assert response.status_code == 200
    assert response.json()["name"] == name


def test_review_id_failure(api_client):
    response = api_client.get("/reviews/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Review not found given id = 999"


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
def test_review_parameters(api_client, parameters, name):
    get_str = "/reviews/?"
    for key, val in parameters.items():
        get_str += f"{key}={val}&"

    response = api_client.get(get_str)
    assert response.status_code == 200
    assert response.json()[0]["name"] == name


def test_review_parameters_failure(api_client):
    response = api_client.get("/reviews/?media_type=1&posted_year=2000")
    assert response.status_code == 200
    assert len(response.json()) == 0
