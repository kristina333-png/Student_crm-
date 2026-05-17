import sys
import asyncio
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
from datetime import date
from practice_project.backend.app.database import SessionLocal, engine, Base
from practice_project.backend.app.models import Group, Student, Grade


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as db:
        from sqlalchemy import select, func
        result = await db.execute(select(func.count(Group.id)))
        if result.scalar() > 0:
            print("База уже содержит данные. Пропускаем заполнение.")
            return

        groups = [
            Group(name="ИТ-31", description="Информационные технологии, 3 курс"),
            Group(name="ИТ-32", description="Информационные технологии, 3 курс"),
            Group(name="ПМ-41", description="Прикладная математика, 4 курс"),
        ]
        db.add_all(groups)
        await db.flush()

        students = [
            Student(first_name="Ivan", last_name="Petrov", email="ivan@example.com", phone="+79161234567", group_id=groups[0].id, enrollment_date=date(2023, 9, 1)),
            Student(first_name="Maria", last_name="Sidorova", email="maria@example.com", phone="+79161234568", group_id=groups[0].id, enrollment_date=date(2023, 9, 1)),
            Student(first_name="Alexey", last_name="Ivanov", email="alex@example.com", phone="+79161234569", group_id=groups[1].id, enrollment_date=date(2023, 9, 1)),
            Student(first_name="Elena", last_name="Kozlova", email="elena@example.com", phone="+79161234570", group_id=groups[1].id, enrollment_date=date(2023, 9, 1)),
            Student(first_name="Dmitry", last_name="Smirnov", email="dmitry@example.com", phone="+79161234571", group_id=groups[2].id, enrollment_date=date(2022, 9, 1)),
            Student(first_name="Anna", last_name="Volkova", email="anna@example.com", phone="+79161234572", group_id=groups[2].id, enrollment_date=date(2022, 9, 1)),
            Student(first_name="Sergey", last_name="Morozov", email="sergey@example.com", phone="+79161234573", group_id=None, enrollment_date=date(2024, 9, 1)),
            Student(first_name="Olga", last_name="Novikova", email="olga@example.com", phone="+79161234574", group_id=None, enrollment_date=date(2024, 9, 1)),
            Student(first_name="Pavel", last_name="Fedorov", email="pavel@example.com", phone="+79161234575", group_id=groups[0].id, enrollment_date=date(2023, 9, 1)),
            Student(first_name="Natalia", last_name="Egorova", email="natalia@example.com", phone="+79161234576", group_id=groups[1].id, enrollment_date=date(2023, 9, 1)),
        ]
        db.add_all(students)
        await db.flush()

        grades = [
            Grade(student_id=students[0].id, subject="Python", score=5.0, grade_date=date(2025, 3, 15)),
            Grade(student_id=students[0].id, subject="Databases", score=4.5, grade_date=date(2025, 3, 20)),
            Grade(student_id=students[1].id, subject="Python", score=4.0, grade_date=date(2025, 3, 15)),
            Grade(student_id=students[1].id, subject="Web", score=5.0, grade_date=date(2025, 3, 22)),
            Grade(student_id=students[2].id, subject="Python", score=3.5, grade_date=date(2025, 3, 15)),
            Grade(student_id=students[3].id, subject="Databases", score=4.5, grade_date=date(2025, 3, 20)),
            Grade(student_id=students[4].id, subject="Math", score=5.0, grade_date=date(2025, 3, 18)),
            Grade(student_id=students[5].id, subject="Math", score=4.0, grade_date=date(2025, 3, 18)),
            Grade(student_id=students[6].id, subject="Python", score=4.5, grade_date=date(2025, 3, 15)),
            Grade(student_id=students[7].id, subject="Web", score=4.0, grade_date=date(2025, 3, 22)),
        ]
        db.add_all(grades)
        await db.commit()
        print("Seed-данные успешно добавлены!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(seed())