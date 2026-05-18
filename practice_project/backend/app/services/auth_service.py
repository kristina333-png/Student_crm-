from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from practice_project.backend.app.models.user import User
from practice_project.backend.app.schemas.user import UserLogin, UserRegister, UserResponse
from practice_project.backend.app.auth_jwt.jwt_handler import verify_password, get_password_hash, create_access_token
from practice_project.backend.app.logger import logger


async def login(db: AsyncSession, data: UserLogin):
    """Логин пользователя, возвращает JWT токен."""
    result = await db.execute(
        select(User).where(User.username == data.username)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
        )

    # Создаём токен с данными пользователя
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id, "role": user.role}
    )

    logger.info(f"Пользователь {user.username} вошёл в систему")

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "full_name": user.full_name,
        }
    }


async def register(db: AsyncSession, data: UserRegister):
    """Регистрация нового пользователя."""
    result = await db.execute(
        select(User).where(User.username == data.username)
    )
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем уже существует",
        )

    hashed_password = get_password_hash(data.password)

    user = User(
        username=data.username,
        password=hashed_password,
        role=data.role or "user",
        full_name=data.full_name,
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    logger.info(f"Зарегистрирован новый пользователь: {user.username}")

    return UserResponse(
        id=user.id,
        username=user.username,
        role=user.role,
        full_name=user.full_name,
    )