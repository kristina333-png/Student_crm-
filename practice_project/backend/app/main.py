from fastapi import FastAPI
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import APP_NAME, APP_VERSION
from app.database import engine, Base
from app.models import Group, Student, Grade

# Создаём все таблицы при старте
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION
)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "app": APP_NAME,
        "version": APP_VERSION
    }