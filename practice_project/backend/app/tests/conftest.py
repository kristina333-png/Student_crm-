import sys
import asyncio

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import pytest
from httpx import AsyncClient, ASGITransport
from practice_project.backend.app.database import get_db, SessionLocal
from practice_project.backend.app.main import app


@pytest.fixture
async def client():
    async def override_get_db():
        async with SessionLocal() as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()