def test_swagger(api_client):
    response = api_client.get("/docs")
    assert response.status_code == 200
