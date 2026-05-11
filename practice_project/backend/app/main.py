import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import APP_NAME, APP_VERSION
from practice_project.backend.app.database import engine, Base
from practice_project.backend.app.models import Group, Student, Grade
from fastapi import FastAPI
from practice_project.backend.app.api.students import router as students_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION
)

app.include_router(students_router)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "app": APP_NAME,
        "version": APP_VERSION
    }