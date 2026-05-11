import uuid
import pytest


@pytest.mark.asyncio
async def test_create_grade(client):
    uid = uuid.uuid4().hex[:8]
    resp = await client.post("/students/", json={
        "first_name": "Grade", "last_name": "Student",
        "email": f"grade_{uid}@example.com",
    })
    student_id = resp.json()["id"]
    response = await client.post("/grades/", json={
        "student_id": student_id, "subject": "Python", "score": 4.5
    })
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_grade_nonexistent_student(client):
    response = await client.post("/grades/", json={
        "student_id": 99999, "subject": "Math", "score": 4.0
    })
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_grade_invalid_score(client):
    uid = uuid.uuid4().hex[:8]
    resp = await client.post("/students/", json={
        "first_name": "Score", "last_name": "Test",
        "email": f"score_{uid}@example.com",
    })
    student_id = resp.json()["id"]
    response = await client.post("/grades/", json={
        "student_id": student_id, "subject": "Math", "score": 10
    })
    assert response.status_code == 422