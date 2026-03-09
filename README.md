# Django REST Shop API

Backend интернет-магазина, реализованный на Django REST Framework.

Проект реализует REST API для работы с пользователями, товарами, корзиной и заказами.

## 🚀 Стек технологий

- Python 3.12
- Django 4+
- Django REST Framework
- PostgreSQL
- JWT авторизация (SimpleJWT)
- Docker / Docker Compose
- drf-spectacular (Swagger документация)
- Django Tests (unittest)

---

# ⚙️ Функционал

## Пользователи

- регистрация
- авторизация (JWT)
- профиль пользователя
- баланс пользователя
- пополнение баланса

## Товары

- просмотр списка товаров
- просмотр одного товара

Только администратор может:

- создавать товары
- редактировать товары
- удалять товары

## Корзина

- добавление товара
- изменение количества
- удаление товара
- просмотр корзины

## Заказы

Создание заказа из корзины с бизнес логикой:

- проверка наличия товара на складе
- проверка баланса пользователя
- списание средств
- уменьшение stock
- очистка корзины
- логирование заказа

---
# 📚 API документация

Swagger доступен по адресу:
http://localhost:8000/api/docs/

---

# 🐳 Запуск проекта через Docker

### 1. Клонировать репозиторий
`git clone https://github.com/Novice-prog/WB_test`

### 2. Создать `.env`
`cp .env.example .env`

### 3. Запуск проекта
`docker compose up --build`

После запуска API будет доступен:
http://localhost:8000

---

# 🧪 Tests

Тесты запускаются автоматически при сборке и запуске Docker контейнера.
Если хотя бы один тест падает, контейнер не запускается.

Также тесты можно запустить вручную:
`docker compose exec backend python manage.py test`

---

# 🔐 Authentication (JWT)

Проект использует JWT авторизацию.

Получить токен можно через:
`POST /api/token/`

Body:

`{
  "username": "your_username",
  "password": "your_password"
}`

Ответ:

`{
  "access": "<access_token>",
  "refresh": "<refresh_token>"
}`

### Для доступа к защищённым endpoints нужно добавить header:

`Authorization: Bearer <access_token>`
