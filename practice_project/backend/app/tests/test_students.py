import uuid
import pytest


@pytest.mark.asyncio
async def test_create_student(client):
    uid = uuid.uuid4().hex[:8]
    response = await client.post("/students/", json={
        "first_name": "Test",
        "last_name": "User",
        "email": f"testuser_{uid}@example.com",
    })
    assert response.status_code == 201
    data = response.json()
    assert "id" in data


@pytest.mark.asyncio
async def test_get_students(client):
    uid = uuid.uuid4().hex[:8]
    await client.post("/students/", json={
        "first_name": "List", "last_name": "Test",
        "email": f"listtest_{uid}@example.com",
    })
    response = await client.get("/students/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) >= 1


@pytest.mark.asyncio
async def test_get_student_by_id(client):
    uid = uuid.uuid4().hex[:8]
    resp = await client.post("/students/", json={
        "first_name": "Get", "last_name": "ById",
        "email": f"getbyid_{uid}@example.com",
    })
    student_id = resp.json()["id"]
    response = await client.get(f"/students/{student_id}")
    assert response.status_code == 200
    assert response.json()["id"] == student_id


@pytest.mark.asyncio
async def test_update_student(client):
    uid = uuid.uuid4().hex[:8]
    resp = await client.post("/students/", json={
        "first_name": "Update", "last_name": "Me",
        "email": f"updateme_{uid}@example.com",
    })
    sid = resp.json()["id"]
    response = await client.put(f"/students/{sid}", json={"first_name": "Updated"})
    assert response.status_code == 200
    assert response.json()["first_name"] == "Updated"


@pytest.mark.asyncio
async def test_delete_student(client):
    uid = uuid.uuid4().hex[:8]
    resp = await client.post("/students/", json={
        "first_name": "Delete", "last_name": "Me",
        "email": f"deleteme_{uid}@example.com",
    })
    sid = resp.json()["id"]
    response = await client.delete(f"/students/{sid}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_duplicate_email_error(client):
    uid = uuid.uuid4().hex[:8]
    email = f"dup_{uid}@example.com"
    await client.post("/students/", json={"first_name": "A", "last_name": "B", "email": email})
    response = await client.post("/students/", json={"first_name": "C", "last_name": "D", "email": email})
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_not_found_error(client):
    response = await client.get("/students/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_validation_error(client):
    response = await client.post("/students/", json={
        "first_name": "", "last_name": "Test", "email": "bad-email"
    })
    assert response.status_code == 422