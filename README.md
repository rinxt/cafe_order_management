
---

# Система управления заказами в кафе

## 📌 Описание проекта

Приложение на Django для управления заказами в кафе позволяет:
- Добавлять, удалять, искать, изменять и отображать заказы;
- Рассчитывать выручку за смену.
- Изменять статус заказа ("в ожидании", "готово", "оплачено");
- Добавлять, удалять, изменять блюда.
> **Примечание:**  
> Удаление блюда происходит через его изменение с присвиванием значения "Аннулировано".  

Помимо стандартного веб-интерфейса, реализовано REST API, через которое можно выполнять те же операции, что и через браузер.

## 🛠️ Стек технологий

- **Python 3.11.0**
- **Django 5.1.6**
- **Django ORM**
- **HTML/CSS**
- **SQLite**
- **Django REST Framework**

## 🚀 Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/rinxt/cafe_order_management.git
```

### 2. Настройка проекта
Установите локальный интерпретатор python с виртуальным окружением для проекта.

Добавьте новую конфигурацию:

Run Configuration -> Django Server.

### 3. Установка зависимостей
Для установки зависимостей выполните следующую команду (зависимости описаны в файле `requirements.txt`):

```bash
pip install -r requirements.txt
```

### 4. Добавление секретного ключа Django
Запустите команду в терминале:
```bash
python -c 'import secrets; print(secrets.token_urlsafe(50))'
```
Скопируйте значение и установите переменную окружения SECRET_KEY в файле .env

### 5. Запуск сервера

Запустите сервер разработки командой:

```bash
python manage.py runserver
```

После этого приложение будет доступно по адресу [http://127.0.0.1:8000](http://127.0.0.1:8000).

URL приложения 
[http://127.0.0.1:8000/cafe_orders/](http://127.0.0.1:8000/cafe_orders/).

## 🚀 Cafe Order Management API

REST API разработано с использованием Django REST Framework и предоставляет следующие возможности, аналогичные веб-интерфейсу:

- **Просмотр списка заказов** с поддержкой фильтрации по номеру стола и статусу;
- **Получение детальной информации** о заказе;
- **Создание нового заказа** с вложенными позициями (блюда и количество);
- **Редактирование заказа**, включая возможность изменения состава заказа и добавление/удаление блюд;
- **Удаление отдельного заказа**;
- **Удаление всех заказов**.

Базовый URL для API:  
`http://127.0.0.1:8000/api`

> **Примечание:**  
> Внутренние значения статуса заказа следующие:  
> • `pending` – *В ожидании*  
> • `ready` – *Готово*  
> • `paid` – *Оплачено*  
>
> При фильтрации через API используйте именно эти значения (на английском).

---

## Эндпоинты API и примеры запросов

### 1. Получение списка заказов

**Endpoint:**  
`GET /api/orders/`

**Описание:**  
Возвращает список заказов, отсортированных по дате создания (сначала новые). Поддерживается фильтрация с помощью GET-параметров:
- `table` – номер стола (целое число от 1 до 15);
- `status` – статус заказа (`pending`, `ready`, `paid`).

**Примеры:**

- Получение всех заказов:
  ```bash
  curl -X GET http://127.0.0.1:8000/api/orders/
  ```

- Фильтрация по номеру стола (например, для стола 5):
  ```bash
  curl -X GET "http://127.0.0.1:8000/api/orders/?table=5"
  ```

- Фильтрация по статусу (например, `pending`):
  ```bash
  curl -X GET "http://127.0.0.1:8000/api/orders/?status=pending"
  ```

- Фильтрация сразу по столу и статусу:
  ```bash
  curl -X GET "http://127.0.0.1:8000/api/orders/?table=5&status=ready"
  ```

### 2. Получение деталей заказа

**Endpoint:**  
`GET /api/orders/{id}/`

**Описание:**  
Возвращает детальную информацию по заказу с указанным ID.

**Пример:**

```bash
curl -X GET http://127.0.0.1:8000/api/orders/1/
```

### 3. Создание нового заказа

**Endpoint:**  
`POST /api/orders/`

**Описание:**  
Создает новый заказ. При создании заказа можно передавать вложенный массив элементов заказа через поле `items`.

**Пример запроса:**

```bash
curl -X POST http://127.0.0.1:8000/api/orders/ \
     -H "Content-Type: application/json" \
     -d '{
           "table_number": 7,
           "status": "pending",
           "items": [
               {"dish": "Кофе", "quantity": 2},
               {"dish": "Чай", "quantity": 1}
           ]
         }'
```

**Ответ:**  
При успешном создании API вернет JSON с данными созданного заказа, включая вычисляемое поле `total_price` и список позиций.

### 4. Редактирование заказа

**Endpoints:**  
`PUT /api/orders/{id}/` или `PATCH /api/orders/{id}/`

**Описание:**  
Позволяет полностью или частично редактировать заказ, включая изменение номера стола, статуса и состава заказа (вложенные позиции).

**Пример запроса:**

```bash
curl -X PATCH http://127.0.0.1:8000/api/orders/1/ \
     -H "Content-Type: application/json" \
     -d '{
           "table_number": 7,
           "status": "ready",
           "items": [
               {"dish": "Кофе", "quantity": 3},
               {"dish": "Сэндвич", "quantity": 1}
           ]
         }'
```

**Ответ:**  
В ответе вы получите обновлённые данные заказа.

### 5. Удаление отдельного заказа

**Endpoint:**  
`DELETE /api/orders/{id}/`

**Описание:**  
Удаляет заказ с указанным ID.

**Пример запроса:**

```bash
curl -X DELETE http://127.0.0.1:8000/api/orders/1/
```

### 6. Удаление всех заказов

**Endpoint (кастомное действие):**  
`POST /api/orders/delete_all/`

**Описание:**  
Удаляет **все** заказы. Это действие реализовано как дополнительное действие (`action`) в `OrderViewSet`.

**Пример запроса:**

```bash
curl -X POST http://127.0.0.1:8000/api/orders/delete_all/
```

**Ответ:**

```json
{"status": "Все заказы удалены"}
```

### 7. Дополнительный поиск

Дополнительное действие `search` позволяет осуществлять поиск по параметру `q`. Если значение параметра – число, производится поиск по столу, иначе – по статусу.

**Примеры:**

```bash
curl -X GET "http://127.0.0.1:8000/api/orders/search/?q=pending"
```

или

```bash
curl -X GET "http://127.0.0.1:8000/api/orders/search/?q=5"
```

---

## Дополнительные замечания

- **Вложенные объекты:**  
  При создании нового заказа обязательно передавайте массив `items`, содержащий объекты с полями `dish` и `quantity`. Сериализатор `OrderItemSerializer` использует поле `dish` как slug-поле, поэтому значение должно точно совпадать с именем блюда, определённым в модели `Dish`.

- **Фильтрация:**  
  Если параметр `status` отсутствует или является пустой строкой, фильтрация по статусу не применяется.

- **Аутентификация:**  
  В текущей конфигурации аутентификация не реализована. При необходимости вы можете добавить её, воспользовавшись стандартными возможностями Django REST Framework.

---
