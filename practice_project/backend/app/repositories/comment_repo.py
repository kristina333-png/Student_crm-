from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from practice_project.backend.app.models.comment import Comment


async def get_comments_by_student(db: AsyncSession, student_id: int) -> list[Comment]:
    result = await db.execute(
        select(Comment).where(Comment.student_id == student_id).order_by(Comment.created_at.desc())
    )
    return result.scalars().all()


async def create_comment(db: AsyncSession, student_id: int, data) -> Comment:
    comment = Comment(student_id=student_id, author_name=data.author_name, text=data.text)
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


async def delete_comment(db: AsyncSession, comment: Comment) -> None:
    await db.delete(comment)
    await db.commit()