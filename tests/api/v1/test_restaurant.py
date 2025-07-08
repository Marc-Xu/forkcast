from fastapi import status


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == {"status": "ok"}


def test_crud_flow(client):
    # Create
    create_data = {"name": "RT", "cuisine": "Z", "rating": 4.0}
    resp = client.post("/restaurants/", json=create_data)
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    rid = data["id"]
    assert data["name"] == "RT"

    # Read
    resp = client.get(f"/restaurants/{rid}")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["id"] == rid

    # List
    resp = client.get("/restaurants/")
    assert resp.status_code == status.HTTP_200_OK
    assert isinstance(resp.json(), list)

    # Patch
    resp = client.patch(f"/restaurants/{rid}", json={"rating": 2.2})
    assert resp.status_code == status.HTTP_200_OK
    assert abs(resp.json()["rating"] - 2.2) < 1e-6

    # Delete
    resp = client.delete(f"/restaurants/{rid}")
    assert resp.status_code == status.HTTP_200_OK
    # Ensure 404 afterwards
    resp = client.get(f"/restaurants/{rid}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND


def test_errors(client):
    # 404 on missing
    resp = client.get("/restaurants/9999")
    assert resp.status_code == status.HTTP_404_NOT_FOUND

    # 422 on bad patch payload
    create_data = {"name": "ERR", "cuisine": "C", "rating": 3.3}
    resp = client.post("/restaurants/", json=create_data)
    rid = resp.json()["id"]
    bad = client.patch(f"/restaurants/{rid}", json={"rating": "not-a-float"})
    assert bad.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_top_by_cuisine(client):
    restaurants = [
        {"name": "X1", "cuisine": "X", "rating": 5.0},
        {"name": "X2", "cuisine": "X", "rating": 4.0},
        {"name": "Y1", "cuisine": "Y", "rating": 3.0},
    ]
    for r in restaurants:
        client.post("/restaurants/", json=r)
    resp = client.get("/restaurants/top?cuisine=X&limit=2")
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    assert len(data) == 2
    assert all(item["cuisine"] == "X" for item in data)
    assert data[0]["rating"] >= data[1]["rating"]


def test_diverse_recommendations_endpoint(client):
    restaurants = [
        {"name": "A1", "cuisine": "A", "rating": 5.0},
        {"name": "A2", "cuisine": "A", "rating": 4.0},
        {"name": "B1", "cuisine": "B", "rating": 3.0},
        {"name": "B2", "cuisine": "B", "rating": 2.0},
        {"name": "C1", "cuisine": "C", "rating": 1.0},
    ]
    for r in restaurants:
        client.post("/restaurants/", json=r)
    resp = client.get("/restaurants/recommend?limit=2")
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    assert len(data) == 2
    assert data[0]["cuisine"] != data[1]["cuisine"]
