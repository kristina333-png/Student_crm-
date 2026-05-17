# API Student CRM

## Базовый URL
`http://127.0.0.1:8000`

## Аутентификация
Все запросы требуют заголовок `X-User-Role`:
- `admin` — полный доступ
- `user` — создание, чтение, обновление
- `guest` — только чтение

## Endpoints

### Студенты `/students`
| Метод | URL | Доступ | Описание |
|-------|-----|--------|----------|
| GET | `/students/` | all | Список (?search, ?group_id, ?page, ?limit, ?sort_by, ?order) |
| GET | `/students/{id}` | all | Один студент |
| POST | `/students/` | admin, user | Создать |
| PUT | `/students/{id}` | admin, user | Обновить |
| DELETE | `/students/{id}` | admin | Удалить |

### Группы `/groups`
| Метод | URL | Доступ | Описание |
|-------|-----|--------|----------|
| GET | `/groups/` | all | Список |
| POST | `/groups/` | admin, user | Создать |
| PUT | `/groups/{id}` | admin, user | Обновить |
| DELETE | `/groups/{id}` | admin | Удалить |

### Оценки `/grades`
| Метод | URL | Доступ | Описание |
|-------|-----|--------|----------|
| GET | `/grades/` | all | Список (?student_id, ?subject) |
| POST | `/grades/` | admin, user | Создать |
| PUT | `/grades/{id}` | admin, user | Обновить |
| DELETE | `/grades/{id}` | admin | Удалить |

### Комментарии `/students/{id}/comments`
| Метод | URL | Доступ | Описание |
|-------|-----|--------|----------|
| GET | `/students/{id}/comments/` | all | Список комментариев |
| POST | `/students/{id}/comments/` | admin, user | Добавить |
| DELETE | `/students/{id}/comments/{comment_id}` | admin | Удалить |

## Формат ответа списка
```json
{
  "items": [],
  "total": 100,
  "page": 1,
  "limit": 10,
  "pages": 10
}


