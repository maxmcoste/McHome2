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
async def test_create_schedule_single_day(client):
    """Create a schedule for Monday only and verify it is persisted with that specific day."""
    house_resp = await client.post("/api/houses", json=make_house_data())
    house_id = house_resp.json()["id"]
    room_resp = await client.post(f"/api/houses/{house_id}/rooms", json=make_room_data())
    room_id = room_resp.json()["id"]

    # Create a Monday-only schedule
    schedule_data = {
        "days_of_week": [0],  # Monday
        "time_start": "09:00:00",
        "time_end": "17:00:00",
        "desired_temp_c": 22.5,
    }
    resp = await client.post(f"/api/houses/{house_id}/rooms/{room_id}/schedules", json=schedule_data)
    assert resp.status_code == 201
    created = resp.json()
    assert created["days_of_week"] == [0]
    assert created["desired_temp_c"] == 22.5
    assert created["time_start"] == "09:00:00"
    assert created["time_end"] == "17:00:00"
    schedule_id = created["id"]

    # Read back via list and verify persisted correctly
    list_resp = await client.get(f"/api/houses/{house_id}/rooms/{room_id}/schedules")
    assert list_resp.status_code == 200
    schedules = list_resp.json()
    assert len(schedules) == 1
    saved = schedules[0]
    assert saved["id"] == schedule_id
    assert saved["days_of_week"] == [0]
    assert saved["desired_temp_c"] == 22.5


@pytest.mark.asyncio
async def test_single_day_schedule_matches_only_that_day(session):
    """Verify get_desired_temp returns the temp only on the matching day, not others."""
    from datetime import time as dt_time
    from mchome2.models import Room, RoomSchedule
    from mchome2.services.room_service import get_desired_temp
    import uuid

    # Create a room directly in the DB
    room = Room(
        id=uuid.uuid4(),
        house_id=uuid.uuid4(),
        name="Test Room",
        volume_m3=50.0,
        insulation_factor=0.5,
        orientation="S",
        window_area_m2=2.0,
    )
    session.add(room)
    await session.flush()

    # Create a Monday-only schedule (day_of_week=0), 09:00-17:00, 22.5C
    schedule = RoomSchedule(
        room_id=room.id,
        days_of_week=[0],
        time_start=dt_time(9, 0),
        time_end=dt_time(17, 0),
        desired_temp_c=22.5,
    )
    session.add(schedule)
    await session.commit()

    # Monday at 12:00 -> should match
    result = await get_desired_temp(session, room.id, day_of_week=0, current_time=dt_time(12, 0))
    assert result == 22.5

    # Tuesday at 12:00 -> should NOT match
    result = await get_desired_temp(session, room.id, day_of_week=1, current_time=dt_time(12, 0))
    assert result is None

    # Monday at 08:00 -> outside time window, should NOT match
    result = await get_desired_temp(session, room.id, day_of_week=0, current_time=dt_time(8, 0))
    assert result is None

    # Sunday at 12:00 -> should NOT match
    result = await get_desired_temp(session, room.id, day_of_week=6, current_time=dt_time(12, 0))
    assert result is None


@pytest.mark.asyncio
async def test_single_day_beats_every_day_schedule(session):
    """When both a specific-day and every-day schedule overlap, the specific day wins."""
    from datetime import time as dt_time
    from mchome2.models import Room, RoomSchedule
    from mchome2.services.room_service import get_desired_temp
    import uuid

    room = Room(
        id=uuid.uuid4(),
        house_id=uuid.uuid4(),
        name="Priority Room",
        volume_m3=50.0,
        insulation_factor=0.5,
        orientation="S",
        window_area_m2=2.0,
    )
    session.add(room)
    await session.flush()

    # Every-day schedule: 08:00-22:00, 20C
    session.add(RoomSchedule(
        room_id=room.id,
        days_of_week=None,
        time_start=dt_time(8, 0),
        time_end=dt_time(22, 0),
        desired_temp_c=20.0,
    ))
    # Monday-only schedule: 08:00-22:00, 24C
    session.add(RoomSchedule(
        room_id=room.id,
        days_of_week=[0],
        time_start=dt_time(8, 0),
        time_end=dt_time(22, 0),
        desired_temp_c=24.0,
    ))
    await session.commit()

    # Monday -> specific-day schedule wins (24C)
    result = await get_desired_temp(session, room.id, day_of_week=0, current_time=dt_time(12, 0))
    assert result == 24.0

    # Wednesday -> falls back to every-day schedule (20C)
    result = await get_desired_temp(session, room.id, day_of_week=2, current_time=dt_time(12, 0))
    assert result == 20.0


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
