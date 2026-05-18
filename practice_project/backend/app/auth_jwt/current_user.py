from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from practice_project.backend.app.auth_jwt.jwt_handler import verify_token
from practice_project.backend.app.database import get_db
from practice_project.backend.app.models.user import User

security = HTTPBearer()


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: AsyncSession = Depends(get_db),
) -> User:
    """Получает текущего пользователя из JWT токена."""
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный или просроченный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен",
        )

    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден",
        )

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Проверяет, что пользователь активен (можно добавить поле is_active позже)."""
    return current_user


def require_role(required_role: str):
    """Фабрика для проверки роли."""

    async def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role != required_role and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Недостаточно прав. Требуется роль: {required_role}",
            )
        return current_user

    return role_checker


def require_permission(action: str):
    """Фабрика для проверки разрешений на действие."""
    permissions = {
        "admin": ["create", "read", "update", "delete"],
        "user": ["create", "read", "update"],
        "guest": ["read"],
    }

    async def permission_checker(current_user: User = Depends(get_current_user)):
        allowed = permissions.get(current_user.role, [])
        if action not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Недостаточно прав для действия '{action}'",
            )
        return current_user

    return permission_checker