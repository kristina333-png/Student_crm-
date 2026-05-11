from datetime import date
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import SessionLocal, engine, Base
from app.models import Group, Student, Grade

def seed():
    # Создаём таблицы, если их ещё нет
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # Проверяем, есть ли уже данные
    if db.query(Group).count() > 0:
        print("База уже содержит данные. Пропускаем заполнение.")
        db.close()
        return

    # Группы
    groups = [
        Group(name="ИТ-31", description="Информационные технологии, 3 курс"),
        Group(name="ИТ-32", description="Информационные технологии, 3 курс"),
        Group(name="ПМ-41", description="Прикладная математика, 4 курс"),
    ]
    db.add_all(groups)
    db.flush()  # чтобы получить id групп

    # Студенты
    students = [
        Student(first_name="Иван", last_name="Петров", email="ivan@example.com",
                phone="+79161234567", group_id=groups[0].id, enrollment_date=date(2023, 9, 1)),
        Student(first_name="Мария", last_name="Сидорова", email="maria@example.com",
                phone="+79161234568", group_id=groups[0].id, enrollment_date=date(2023, 9, 1)),
        Student(first_name="Алексей", last_name="Иванов", email="alex@example.com",
                phone="+79161234569", group_id=groups[1].id, enrollment_date=date(2023, 9, 1)),
        Student(first_name="Елена", last_name="Козлова", email="elena@example.com",
                phone="+79161234570", group_id=groups[1].id, enrollment_date=date(2023, 9, 1)),
        Student(first_name="Дмитрий", last_name="Смирнов", email="dmitry@example.com",
                phone="+79161234571", group_id=groups[2].id, enrollment_date=date(2022, 9, 1)),
        Student(first_name="Анна", last_name="Волкова", email="anna@example.com",
                phone="+79161234572", group_id=groups[2].id, enrollment_date=date(2022, 9, 1)),
        Student(first_name="Сергей", last_name="Морозов", email="sergey@example.com",
                phone="+79161234573", group_id=None, enrollment_date=date(2024, 9, 1)),
        Student(first_name="Ольга", last_name="Новикова", email="olga@example.com",
                phone="+79161234574", group_id=None, enrollment_date=date(2024, 9, 1)),
        Student(first_name="Павел", last_name="Фёдоров", email="pavel@example.com",
                phone="+79161234575", group_id=groups[0].id, enrollment_date=date(2023, 9, 1)),
        Student(first_name="Наталья", last_name="Егорова", email="natalia@example.com",
                phone="+79161234576", group_id=groups[1].id, enrollment_date=date(2023, 9, 1)),
    ]
    db.add_all(students)
    db.flush()

    # Оценки
    grades = [
        Grade(student_id=students[0].id, subject="Python", score=5.0, date=date(2025, 3, 15)),
        Grade(student_id=students[0].id, subject="Базы данных", score=4.5, date=date(2025, 3, 20)),
        Grade(student_id=students[1].id, subject="Python", score=4.0, date=date(2025, 3, 15)),
        Grade(student_id=students[1].id, subject="Веб-разработка", score=5.0, date=date(2025, 3, 22)),
        Grade(student_id=students[2].id, subject="Python", score=3.5, date=date(2025, 3, 15)),
        Grade(student_id=students[3].id, subject="Базы данных", score=4.5, date=date(2025, 3, 20)),
        Grade(student_id=students[4].id, subject="Математика", score=5.0, date=date(2025, 3, 18)),
        Grade(student_id=students[5].id, subject="Математика", score=4.0, date=date(2025, 3, 18)),
        Grade(student_id=students[6].id, subject="Python", score=4.5, date=date(2025, 3, 15)),
        Grade(student_id=students[7].id, subject="Веб-разработка", score=4.0, date=date(2025, 3, 22)),
    ]
    db.add_all(grades)

    db.commit()
    db.close()
    print("Seed-данные успешно добавлены!")

if __name__ == "__main__":
    seed()