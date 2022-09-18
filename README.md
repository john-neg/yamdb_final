![example workflow](https://github.com/john-neg/yamdb_final/workflows/yamdb_workflow.yml/badge.svg)

# api_yamdb

База данных произведений _(Practicum by Yandex education project)_

## Технологии:

YaMDB учебный проект базирующийся на:
- Python 3.7
- Django 2.2.16

## Описание:

REST API сервис для YaMDB (база данных музыки, книг, фильмов и т.д.).

Полная CRUD имплементация для моделей Title, User.

Зарегистрированные пользователи могут публиковать отзывы

Незарегистрированные пользователи могут оставлять комментарии к отзывам.


---

## Установка и запуск с помощью Docker

### Установить переменные окружения

```sh
nano infra/.env
```

#### Содержимое файла .env

```
SECRET_KEY='key'
DEBUG=False
ALLOWED_HOSTS='localhost web 127.0.0.1'
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres-pass
DB_HOST=db
DB_PORT=5432
```

### Запуск docker-compose

```sh
cd infra
docker-compose up -d --build
```

### Применения миграций

```sh
docker-compose exec web python manage.py migrate
```

### Загрузка данных в БД

```sh
docker-compose exec web python manage.py manage.py loaddata db.json
```

### Создание суперпользователя

```sh
docker-compose exec web python manage.py createsuperuser --username=admin --email=admin@local.host
```

### Сбор статики в /static/

```sh
docker-compose exec web python manage.py collectstatic --no-input
```

---

## Авторизация 

### Получение код подтверждения

#### GET /api/v1/auth/signup/

##### PAYLOAD

```json
{
    "email": "string",
    "username": "string"
}
```

На адрес электронной почты придет код регистрации

### Получение токена

#### GET /api/v1/auth/token/

##### PAYLOAD

```json
{
    "username": "string",
    "confirmation_code": "string"
}
```

##### RESPONSE

```json
{
  "token": "string"
}
```

---

## Примеры запросов

### Получение списка произведений Titles

#### GET /api/v1/titles/

##### QUERY PARAMETERS

category (string)
_фильтрует по полю slug категории_

genre (string)
_фильтрует по полю slug жанра_

name (string)
_фильтрует по названию произведения_

year (integer)
_фильтрует по году_

##### RESPONSE

```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
          {
            "name": "string",
            "slug": "string"
          }
        ],
        "category": {
          "name": "string",
          "slug": "string"
        }
      }
    ]
  }
]
```

#### POST /api/v1/titles/

##### QUERY PARAMETERS

name (required, string)
_Название_

year (required, integer)
_Год выпуска_

description (string)
_Описание_

genre (required, Array of strings)
_Slug жанра_

category (required, string)
_Slug категории_

##### PAYLOAD

```json
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

##### RESPONSE

```json
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```

## Author info:
Evgeny Semenov

## License
MIT