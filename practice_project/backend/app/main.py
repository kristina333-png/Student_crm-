from practice_project.backend.app.config import APP_NAME, APP_VERSION
from practice_project.backend.app.database import engine, Base
from practice_project.backend.app.models import Group, Student, Grade
from fastapi import FastAPI
from practice_project.backend.app.api.students import router as students_router
from practice_project.backend.app.api.groups import router as groups_router
from practice_project.backend.app.api.grades import router as grades_router

app = FastAPI(title=APP_NAME, version=APP_VERSION)

app.include_router(students_router)
app.include_router(groups_router)
app.include_router(grades_router)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/health")
def health_check():
    return {"status": "ok", "app": APP_NAME, "version": APP_VERSION}