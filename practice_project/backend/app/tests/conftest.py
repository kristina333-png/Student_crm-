import sys
import asyncio

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import pytest
from httpx import AsyncClient, ASGITransport
from practice_project.backend.app.database import get_db, SessionLocal
from practice_project.backend.app.main import app
from practice_project.backend.app.auth_jwt.jwt_handler import create_access_token


@pytest.fixture
async def client():
    async def override_get_db():
        async with SessionLocal() as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)

    # Создаём токен для admin
    access_token = create_access_token(data={"sub": "admin", "user_id": 1, "role": "admin"})
    headers = {"Authorization": f"Bearer {access_token}"}

    async with AsyncClient(transport=transport, base_url="http://test", headers=headers) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
async def clean_after_test():
    yield
    async with SessionLocal() as db:
        from sqlalchemy import text
        await db.execute(
            text("DELETE FROM grades WHERE student_id IN (SELECT id FROM students WHERE email LIKE '%@example.com')"))
        await db.execute(text("DELETE FROM students WHERE email LIKE '%@example.com'"))
        await db.execute(text("DELETE FROM groups WHERE name LIKE 'Test-%' OR name LIKE 'List-%' OR name LIKE 'Dup-%'"))
        await db.commit()