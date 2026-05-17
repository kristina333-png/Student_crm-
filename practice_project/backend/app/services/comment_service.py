from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from practice_project.backend.app.schemas.comment import CommentCreate
from practice_project.backend.app.repositories import comment_repo, student_repo
from practice_project.backend.app.logger import logger


async def get_comments(db: AsyncSession, student_id: int):
    return await comment_repo.get_comments_by_student(db, student_id)


async def create_comment(db: AsyncSession, student_id: int, data: CommentCreate):
    student = await student_repo.get_student_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")
    comment = await comment_repo.create_comment(db, student_id, data)
    logger.info(f"Добавлен комментарий к студенту id={student_id}")
    return comment


async def delete_comment(db: AsyncSession, comment_id: int):
    from practice_project.backend.app.models.comment import Comment
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    await comment_repo.delete_comment(db, comment)