# Student CRM

Учебный fullstack-проект. Система управления студентами: группы, оценки, посещаемость.

## Стек
- **Backend:** Python 3.11+, FastAPI, PostgreSQL, SQLAlchemy (async)
- **Frontend:** Vue 3, Vite (будет позже)

## Быстрый старт

### 1. Клонировать репозиторий

    git clone https://github.com/kristina333-png/Student_crm-.git
    cd Student_crm-/practice_project

### 2. Настроить окружение

    cd backend
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt

### 3. Настроить .env

Скопируй .env.example в .env и укажи DATABASE_URL для PostgreSQL.

### 4. Создать таблицы и заполнить данными

    cd app
    python seed.py

### 5. Запустить backend

    uvicorn main:app --reload