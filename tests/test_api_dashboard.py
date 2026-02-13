import pytest

from tests.conftest import make_house_data


@pytest.mark.asyncio
async def test_dashboard_empty(client):
    resp = await client.get("/api/dashboard")
    assert resp.status_code == 200
    data = resp.json()
    assert data["houses"] == []


@pytest.mark.asyncio
async def test_dashboard_with_house(client):
    # Create a house first
    house_resp = await client.post("/api/houses", json=make_house_data())
    assert house_resp.status_code == 201
    house_id = house_resp.json()["id"]

    # Get dashboard
    resp = await client.get("/api/dashboard")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["houses"]) == 1
    assert data["houses"][0]["house_name"] == "Test House"
    assert data["houses"][0]["rooms"] == []


@pytest.mark.asyncio
async def test_house_dashboard(client):
    # Create a house
    house_resp = await client.post("/api/houses", json=make_house_data("Dashboard House"))
    house_id = house_resp.json()["id"]

    resp = await client.get(f"/api/dashboard/{house_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["house_name"] == "Dashboard House"


@pytest.mark.asyncio
async def test_house_dashboard_not_found(client):
    resp = await client.get("/api/dashboard/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404
