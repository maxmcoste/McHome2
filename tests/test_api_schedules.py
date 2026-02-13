import pytest

from tests.conftest import make_house_data, make_room_data


@pytest.mark.asyncio
async def test_delete_schedule(client):
    house_resp = await client.post("/api/houses", json=make_house_data())
    house_id = house_resp.json()["id"]
    room_resp = await client.post(f"/api/houses/{house_id}/rooms", json=make_room_data())
    room_id = room_resp.json()["id"]

    sched_resp = await client.post(
        f"/api/houses/{house_id}/rooms/{room_id}/schedules",
        json={"days_of_week": [0, 1, 2, 3, 4], "time_start": "08:00:00", "time_end": "22:00:00", "desired_temp_c": 21.0},
    )
    assert sched_resp.status_code == 201
    schedule_id = sched_resp.json()["id"]

    del_resp = await client.delete(f"/api/houses/{house_id}/rooms/{room_id}/schedules/{schedule_id}")
    assert del_resp.status_code == 204

    list_resp = await client.get(f"/api/houses/{house_id}/rooms/{room_id}/schedules")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 0


@pytest.mark.asyncio
async def test_delete_schedule_not_found(client):
    house_resp = await client.post("/api/houses", json=make_house_data("Sched House"))
    house_id = house_resp.json()["id"]
    room_resp = await client.post(f"/api/houses/{house_id}/rooms", json=make_room_data("Sched Room"))
    room_id = room_resp.json()["id"]

    resp = await client.delete(
        f"/api/houses/{house_id}/rooms/{room_id}/schedules/00000000-0000-0000-0000-000000000000"
    )
    assert resp.status_code == 404
