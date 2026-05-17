# Student CRM

Учебный fullstack-проект. Система управления студентами: группы, оценки, посещаемость.

## Стек
- **Backend:** Python 3.11+, FastAPI, PostgreSQL, SQLAlchemy (async)
- **Frontend:** Vue 3, Vite (будет позже)

## Быстрый старт

### Backend
cd practice_project/backend
venv\Scripts\activate
uvicorn practice_project.backend.app.main:app --reload

### Frontend
cd practice_project/frontend
npm run dev

## Тестовые данные
python backend/app/seed.py

## Тесты
python -m pytest backend/app/tests/ -v