from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from practice_project.backend.app.models.student import Student
from practice_project.backend.app.models.group import Group


async def get_students(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10,
    search: str | None = None,
    group_id: int | None = None,
    sort_by: str = "id",
    order: str = "asc",
) -> tuple[list[Student], int]:
    query = select(Student)

    if search:
        query = query.where(
            Student.first_name.ilike(f"%{search}%")
            | Student.last_name.ilike(f"%{search}%")
            | Student.email.ilike(f"%{search}%")
        )
    if group_id is not None:
        query = query.where(Student.group_id == group_id)

    sort_column = getattr(Student, sort_by, Student.id)
    query = query.order_by(sort_column.desc() if order == "desc" else sort_column.asc())

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    students = result.scalars().all()

    for student in students:
        if student.group_id:
            grp = await db.get(Group, student.group_id)
            student.group_name = grp.name if grp else None
        else:
            student.group_name = None

    return students, total


async def get_student_by_id(db: AsyncSession, student_id: int) -> Student | None:
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if student and student.group_id:
        grp = await db.get(Group, student.group_id)
        student.group_name = grp.name if grp else None
    return student


async def get_student_by_email(db: AsyncSession, email: str) -> Student | None:
    result = await db.execute(select(Student).where(Student.email == email))
    return result.scalar_one_or_none()


async def create_student(db: AsyncSession, student_data) -> Student:
    student = Student(**student_data.model_dump())
    db.add(student)
    await db.commit()
    await db.refresh(student)
    return student


async def update_student(db: AsyncSession, student: Student, update_data) -> Student:
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(student, field, value)
    await db.commit()
    await db.refresh(student)
    return student


async def delete_student(db: AsyncSession, student: Student) -> None:
    await db.delete(student)
    await db.commit()