from fastapi import Request, HTTPException, status

# Какие роли к каким эндпоинтам имеют доступ
ROLE_PERMISSIONS = {
    "admin": ["create", "read", "update", "delete"],
    "user": ["create", "read", "update"],
    "guest": ["read"],
}


def get_current_role(request: Request) -> str:
    """Извлекает роль пользователя из заголовка X-User-Role."""
    role = request.headers.get("X-User-Role", "guest")
    if role not in ROLE_PERMISSIONS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Неизвестная роль: {role}",
        )
    return role


def require_permission(required: str):
    """Проверяет, имеет ли текущая роль доступ к действию."""
    role = get_current_role  # будет вызвана позже
    return role


def check_permission(role: str, action: str) -> bool:
    """Проверяет, разрешено ли действие для роли."""
    return action in ROLE_PERMISSIONS.get(role, [])