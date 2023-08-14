# Описание
Проект YaMDb собирает отзывы пользователей на различные произведения.

# Алгоритм регистрации пользователей
Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами email и username на эндпоинт /api/v1/auth/signup/.

YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.

Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).

При желании пользователь отправляет PATCH-запрос на эндпоинт /api/v1/users/me/ и заполняет поля в своём профайле (описание полей — в документации).


# Как запустить проект
Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:altdinov/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

# Импорт из CSV
Для удобства работы в проекте реализован функционал импорта заранее подготовленных данных из csv файлов.
Для импорта используейте команду:

```
python manage.py import_from_csv "static/data/category.csv" "static/data/genre.csv" "static/data/titles.csv" "static/data/genre_title.csv" "static/data/users.csv"
```

# Примеры
Ниже показаны некоторые примеры запросов к API.

## Регистрация нового пользователя
**POST**  http://127.0.0.1:8000/api/v1/auth/signup/

_Request samples:_
```
{
    "email": "user@example.com",
    "username": "string"
}
```

_Response samples:_
```
{
    "email": "string",
    "username": "string"
}
```

## Получение JWT-токена
**POST**  http://127.0.0.1:8000/api/v1/auth/token/

_Request samples:_
```
{
    "username": "string",
    "confirmation_code": "string"
}
```

_Response samples:_
```
{
    "token": "string"
}
```

## Получение списка всех произведений
**GET**  http://127.0.0.1:8000/api/v1/titles/

_Response samples:_
```
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
        "category": 
            {
                "name": "string",
                "slug": "string"
            }
        }
    ]
}
```

Список всех запросов к API доступен по ссылке: http://127.0.0.1:8000/redoc/
