ROLE_PERMISSIONS = {
    "admin": ["create", "read", "update", "delete"],
    "teacher": ["read", "update"],  # учитель может читать и редактировать
    "student": ["read"],            # студент только читает
}


def check_permission(role: str, action: str) -> bool:
    """Проверяет, разрешено ли действие для роли."""
    return action in ROLE_PERMISSIONS.get(role, [])