import pytest

from tests.conftest import make_house_data, make_room_data


@pytest.mark.asyncio
async def test_create_room(client):
    house_resp = await client.post("/api/houses", json=make_house_data())
    house_id = house_resp.json()["id"]

    resp = await client.post(f"/api/houses/{house_id}/rooms", json=make_room_data())
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Living Room"
    assert data["house_id"] == house_id
    assert data["volume_m3"] == 60.0


@pytest.mark.asyncio
async def test_list_rooms(client):
    house_resp = await client.post("/api/houses", json=make_house_data())
    house_id = house_resp.json()["id"]
    await client.post(f"/api/houses/{house_id}/rooms", json=make_room_data("Room A"))
    await client.post(f"/api/houses/{house_id}/rooms", json=make_room_data("Room B"))

    resp = await client.get(f"/api/houses/{house_id}/rooms")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


@pytest.mark.asyncio
async def test_get_room(client):
    house_resp = await client.post("/api/houses", json=make_house_data())
    house_id = house_resp.json()["id"]
    room_resp = await client.post(f"/api/houses/{house_id}/rooms", json=make_room_data())
    room_id = room_resp.json()["id"]

    resp = await client.get(f"/api/houses/{house_id}/rooms/{room_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Living Room"


@pytest.mark.asyncio
async def test_update_room(client):
    house_resp = await client.post("/api/houses", json=make_house_data())
    house_id = house_resp.json()["id"]
    room_resp = await client.post(f"/api/houses/{house_id}/rooms", json=make_room_data())
    room_id = room_resp.json()["id"]

    resp = await client.put(f"/api/houses/{house_id}/rooms/{room_id}", json={"name": "Kitchen"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "Kitchen"


@pytest.mark.asyncio
async def test_delete_room(client):
    house_resp = await client.post("/api/houses", json=make_house_data())
    house_id = house_resp.json()["id"]
    room_resp = await client.post(f"/api/houses/{house_id}/rooms", json=make_room_data())
    room_id = room_resp.json()["id"]

    resp = await client.delete(f"/api/houses/{house_id}/rooms/{room_id}")
    assert resp.status_code == 204
    resp = await client.get(f"/api/houses/{house_id}/rooms/{room_id}")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_create_schedule_every_day(client):
    house_resp = await client.post("/api/houses", json=make_house_data())
    house_id = house_resp.json()["id"]
    room_resp = await client.post(f"/api/houses/{house_id}/rooms", json=make_room_data())
    room_id = room_resp.json()["id"]

    schedule_data = {
        "days_of_week": None,
        "time_start": "06:00:00",
        "time_end": "22:00:00",
        "desired_temp_c": 21.0,
    }
    resp = await client.post(f"/api/houses/{house_id}/rooms/{room_id}/schedules", json=schedule_data)
    assert resp.status_code == 201
    data = resp.json()
    assert data["desired_temp_c"] == 21.0
    assert data["days_of_week"] is None


@pytest.mark.asyncio
async def test_create_schedule_workdays(client):
    house_resp = await client.post("/api/houses", json=make_house_data())
    house_id = house_resp.json()["id"]
    room_resp = await client.post(f"/api/houses/{house_id}/rooms", json=make_room_data())
    room_id = room_resp.json()["id"]

    schedule_data = {
        "days_of_week": [0, 1, 2, 3, 4],
        "time_start": "07:00:00",
        "time_end": "18:00:00",
        "desired_temp_c": 22.0,
    }
    resp = await client.post(f"/api/houses/{house_id}/rooms/{room_id}/schedules", json=schedule_data)
    assert resp.status_code == 201
    data = resp.json()
    assert data["days_of_week"] == [0, 1, 2, 3, 4]
    assert data["desired_temp_c"] == 22.0


@pytest.mark.asyncio
async def test_create_schedule_weekends(client):
    house_resp = await client.post("/api/houses", json=make_house_data())
    house_id = house_resp.json()["id"]
    room_resp = await client.post(f"/api/houses/{house_id}/rooms", json=make_room_data())
    room_id = room_resp.json()["id"]

    schedule_data = {
        "days_of_week": [5, 6],
        "time_start": "09:00:00",
        "time_end": "23:00:00",
        "desired_temp_c": 23.0,
    }
    resp = await client.post(f"/api/houses/{house_id}/rooms/{room_id}/schedules", json=schedule_data)
    assert resp.status_code == 201
    data = resp.json()
    assert data["days_of_week"] == [5, 6]


@pytest.mark.asyncio
async def test_list_schedules(client):
    house_resp = await client.post("/api/houses", json=make_house_data())
    house_id = house_resp.json()["id"]
    room_resp = await client.post(f"/api/houses/{house_id}/rooms", json=make_room_data())
    room_id = room_resp.json()["id"]

    schedule_data = {
        "time_start": "06:00:00",
        "time_end": "22:00:00",
        "desired_temp_c": 21.0,
    }
    await client.post(f"/api/houses/{house_id}/rooms/{room_id}/schedules", json=schedule_data)

    resp = await client.get(f"/api/houses/{house_id}/rooms/{room_id}/schedules")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


@pytest.mark.asyncio
async def test_room_current_no_readings(client):
    house_resp = await client.post("/api/houses", json=make_house_data())
    house_id = house_resp.json()["id"]
    room_resp = await client.post(f"/api/houses/{house_id}/rooms", json=make_room_data())
    room_id = room_resp.json()["id"]

    resp = await client.get(f"/api/houses/{house_id}/rooms/{room_id}/current")
    assert resp.status_code == 200
    data = resp.json()
    assert data["temperature_c"] is None
    assert data["windows_open"] == 0
