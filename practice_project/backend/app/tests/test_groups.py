import uuid
import pytest


@pytest.mark.asyncio
async def test_create_group(client):
    uid = uuid.uuid4().hex[:8]
    response = await client.post("/groups/", json={"name": f"Test-{uid}"})
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_get_groups(client):
    uid = uuid.uuid4().hex[:8]
    await client.post("/groups/", json={"name": f"List-{uid}"})
    response = await client.get("/groups/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_duplicate_group_error(client):
    uid = uuid.uuid4().hex[:8]
    name = f"Dup-{uid}"
    await client.post("/groups/", json={"name": name})
    response = await client.post("/groups/", json={"name": name})
    assert response.status_code == 400