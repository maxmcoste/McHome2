import pytest


@pytest.mark.asyncio
async def test_get_settings(client):
    resp = await client.get("/api/settings")
    assert resp.status_code == 200
    data = resp.json()
    assert "database_url" in data
    assert "sensor_poll_interval_seconds" in data
    assert "prediction_interval_seconds" in data


@pytest.mark.asyncio
async def test_update_settings(client):
    resp = await client.put("/api/settings", json={
        "sensor_poll_interval_seconds": 60,
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["sensor_poll_interval_seconds"] == 60
