# Fast-Api-Shop

📚 Стек технологий
- Python 3.10+

- FastAPI — фреймворк для API

- SQLAlchemy — ORM

- Alembic — миграции БД

- Pydantic — валидация данных

- PostgreSQL

- Uvicorn — сервер

- passlib[bcrypt] — хеширование паролей

- python-jose — JWT-токены

- pydantic-settings - проверка к подключение к бд

- dotenv - загрузка из .env

- asyncpg - асинхронный движок для PostgreSQL


## Cтруктура проекта

```bash
├── app/
│   ├── api/                # Роуты
│   │   ├── auth.py
│   │   ├── products.py
│   │   ├── orders.py
│   │   ├── cart.py
│   │   └── admin.py
│   ├── models/             # SQLAlchemy модели
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── category.py
│   │   ├── order.py
│   │   ├── order_item.py
│   │   └── cart.py
│   ├── schemas/            # Pydantic-схемы
│   │   └── ...
│   ├── services/           # Бизнес-логика
│   │   └── ...
│   ├── core/               # Настройки, база, JWT и т.п.
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py
│   │   └── deps.py
│   └── main.py             # Входная точка FastAPI
├── alembic/                # Миграции
├── requirements.txt
└── README.md

```
👥 Роли
User (покупатель) — регистрация, просмотр товаров, корзина, оформление заказов

Admin — управление товарами, категориями, пользователями, заказами






```bash
# Установка зависимостей
pip install -r requirements.txt

# Инициализация БД
alembic upgrade head

# Запуск сервера
uvicorn app.main:app --reload
```
