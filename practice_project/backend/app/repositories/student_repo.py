from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from practice_project.backend.app.models.student import Student
from practice_project.backend.app.models.group import Group


async def get_students(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    search: str | None = None,
    group_id: int | None = None,
):
    query = select(Student)
    if search:
        query = query.where(
            Student.first_name.ilike(f"%{search}%")
            | Student.last_name.ilike(f"%{search}%")
            | Student.email.ilike(f"%{search}%")
        )
    if group_id is not None:
        query = query.where(Student.group_id == group_id)
    query = query.offset(skip).limit(limit).order_by(Student.id)
    result = await db.execute(query)
    students = result.scalars().all()

    for student in students:
        if student.group_id:
            grp = await db.get(Group, student.group_id)
            student.group_name = grp.name if grp else None
        else:
            student.group_name = None

    return students


async def get_student_by_id(db: AsyncSession, student_id: int):
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if student:
        if student.group_id:
            grp = await db.get(Group, student.group_id)
            student.group_name = grp.name if grp else None
    return student


async def get_student_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(Student).where(Student.email == email))
    return result.scalar_one_or_none()


async def create_student(db: AsyncSession, student_data):
    student = Student(**student_data.model_dump())
    db.add(student)
    await db.commit()
    await db.refresh(student)
    return student


async def update_student(db: AsyncSession, student: Student, update_data):
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(student, field, value)
    await db.commit()
    await db.refresh(student)
    return student


async def delete_student(db: AsyncSession, student: Student):
    await db.delete(student)
    await db.commit()
    return student