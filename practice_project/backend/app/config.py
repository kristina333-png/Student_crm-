import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(env_path)

APP_NAME = os.getenv("APP_NAME", "student_crm")
APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
DATABASE_URL = os.getenv("DATABASE_URL")