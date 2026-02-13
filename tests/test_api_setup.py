import pytest


@pytest.mark.asyncio
async def test_setup_status(client):
    resp = await client.get("/api/setup/status")
    assert resp.status_code == 200
    data = resp.json()
    assert "db_connected" in data
    assert "migrations_done" in data
    assert "houses_exist" in data
    assert "setup_complete" in data


@pytest.mark.asyncio
async def test_check_db(client):
    resp = await client.post("/api/setup/check-db")
    assert resp.status_code == 200
    data = resp.json()
    # With SQLite test DB, connectivity check may fail since it uses the real settings URL
    assert "connected" in data
