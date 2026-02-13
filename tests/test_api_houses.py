import pytest

from tests.conftest import make_house_data


@pytest.mark.asyncio
async def test_create_house(client):
    resp = await client.post("/api/houses", json=make_house_data())
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Test House"
    assert data["latitude"] == 41.9028
    assert data["longitude"] == 12.4964
    assert data["timezone"] == "Europe/Rome"
    assert "id" in data


@pytest.mark.asyncio
async def test_list_houses(client):
    await client.post("/api/houses", json=make_house_data("House A"))
    await client.post("/api/houses", json=make_house_data("House B"))
    resp = await client.get("/api/houses")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_get_house(client):
    create_resp = await client.post("/api/houses", json=make_house_data())
    house_id = create_resp.json()["id"]
    resp = await client.get(f"/api/houses/{house_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Test House"
    assert data["room_count"] == 0
    assert data["device_count"] == 0


@pytest.mark.asyncio
async def test_update_house(client):
    create_resp = await client.post("/api/houses", json=make_house_data())
    house_id = create_resp.json()["id"]
    resp = await client.put(f"/api/houses/{house_id}", json={"name": "Updated House"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "Updated House"


@pytest.mark.asyncio
async def test_delete_house(client):
    create_resp = await client.post("/api/houses", json=make_house_data())
    house_id = create_resp.json()["id"]
    resp = await client.delete(f"/api/houses/{house_id}")
    assert resp.status_code == 204
    resp = await client.get(f"/api/houses/{house_id}")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_get_nonexistent_house(client):
    resp = await client.get("/api/houses/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404
