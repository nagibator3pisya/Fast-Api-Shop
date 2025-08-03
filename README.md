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
# 👥 Роли
User (покупатель) — регистрация, просмотр товаров, корзина, оформление заказов

Admin — управление товарами, категориями, пользователями, заказами


# 🗂️ Модели и связи
1. User
id, email, hashed_password, is_active, is_admin

2. Category
id, name, description

3. Product
id, name, description, price, quantity, is_active, category_id

4. CartItem (корзина пользователя)
- id

- user_id → FK → User

- product_id → FK → Product

- quantity

    Корзина — просто таблица CartItem, 
    где указывается пользователь и выбранный товар. 
    Очищается при оформлении заказа.

5.  Order
id, user_id, status, created_at, updated_at

6. OrderItem
id, order_id, product_id, quantity, price_at_order

# 📦 Возможные статусы заказа (Order.status)
Статус	        Описание
new	            Заказ создан, но ещё не оплачен
paid	        Заказ оплачен
processing	    Заказ в обработке (собирается на складе)
shipped	        Отправлен курьером / службой доставки
delivered	    Доставлен покупателю
cancelled	    Отменён покупателем или магазином
returned	    Покупатель вернул товар
failed	        Ошибка при оплате или доставке



# 🔐 Аутентификация
- JWT токены

- POST /auth/register, POST /auth/login

- Authorization: Bearer <token> в заголовке

# 📦 Эндпоинты

## 🔓 Аутентификация
| Метод  | Путь             | Описание    |
|--------|------------------|-------------|
| `POST` | `/auth/register` | Регистрация |
| `POST` | `/auth/login`    | Вход        |

## 🛍️ Товары и категории
| Метод    | Путь                            | Описание                     |
|----------|---------------------------------|------------------------------|
| `GET`    | `/products/`                    | Все товары                   |
| `GET`    | `/categories/`                  | Все категории                |
| `POST`   | `/admin/add_products/`          | Добавить товар *(admin)*     |
| `PUT`    | `/admin/update_products/{id}`   | Обновить товар *(admin)*     |
| `DELETE` | `/admin/delete_products/{id}`   | Удалить  товар *(admin)*     |
| `POST`   | `/admin/add_categories/`        | Добавить категорию *(admin)* |
| `PUT`    | `/admin/update_categories/{id}` | Обновить категорию *(admin)* |
| `DELETE` | `/admin/delete_categories/{id}` | Удалить категорию *(admin)*  |

## 🛒 Корзина

| Метод    | Путь              | Описание                  |
|----------|-------------------|---------------------------|
| `GET`    | `/cart/`          | Моя корзина               |
| `POST`   | `/cart/`          | Добавить товар в корзину  |
| `PUT`    | `/cart/{item_id}` | Изменить кол-во товара    |
| `DELETE` | `/cart/{item_id}` | Удалить товар из корзины  |
| `POST`   | `/cart/checkout`  | Оформить заказ из корзины |

## 📦 Заказы

| Метод | Путь                 | Описание             |
|-------|----------------------|----------------------|
| `GET` | `/orders/my`         | Мои заказы           |
| `GET` | `/admin/all_orders/` | Все заказы *(admin)* |



```bash
# Установка зависимостей
pip install -r requirements.txt

# Инициализация БД
alembic upgrade head

# Запуск сервера
uvicorn app.main:app --reload
```
