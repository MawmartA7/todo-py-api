# todo-py-api

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2%2B-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14%2B-orange.svg)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13%2B-blue.svg)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Translation to pt-BR](README.pt-br.md)

A simple Django RESTful API for managing personal tasks, with JWT authentication.

---

## Features

- User registration & JWT authentication
- CRUD for tasks (Create, Read, Update, Delete)
- Pagination & filtering for task list
- Field validation with detailed error messages

---

## Technologies

- Python 3.8+
- Django 4.2+
- Django REST Framework 3.14+
- PostgreSQL (production)

--- 

## Authentication

### User Field Validation

- **username**:
  - Required
  - Max 150 characters
  - Only letters, digits, and `@/./+/-/_` characters allowed
  - Unique (cannot already exist)
- **password**:
  - Required
  - Max 128 characters
  - No additional constraints by default

#### Example Error Responses

**Username too long**

Status: `400 Bad Request`
```json
{
  "username": ["Ensure this field has no more than 150 characters."]
}
```

**Username contains invalid characters**

Status: `400 Bad Request`
```json
{
  "username": ["Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters."]
}
```

**Username required**

Status: `400 Bad Request`
```json
{
  "username": ["This field is required."]
}
```

**Password required**

Status: `400 Bad Request`
```json
{
  "password": ["This field is required."]
}
```

**Password too long**

Status: `400 Bad Request`
```json
{
  "password": ["Ensure this field has no more than 128 characters."]
}
```

---

### Register

- **POST** `/api/auth/register/`

#### Request

```json
{
  "username": "newuser",
  "password": "newpassword"
}
```

#### Success Response

Status: `201 Created`
```json
{
  "id": 1,
  "username": "newuser"
}
```

#### Error Responses

Status: `400 Bad Request`
```json
{
  "username": ["A user with that username already exists."]
}
```

---

### Login

- **POST** `/api/auth/login/`

#### Request

```json
{
  "username": "newuser",
  "password": "newpassword"
}
```

#### Success Response

Status: `200 OK`
```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

#### Error Response

Status: `401 Unauthorized`
```json
{
  "detail": "No active account found with the given credentials"
}
```

---

### Token Refresh

- **POST** `/api/auth/token/refresh/`

#### Request

```json
{
  "refresh": "<refresh_token>"
}
```

#### Success Response

Status: `200 OK`
```json
{
  "access": "<new_access_token>"
}
```

#### Error Response

Status: `401 Unauthorized`
```json
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

---

### Token Verify

- **POST** `/api/auth/token/verify/`

#### Request

```json
{
  "token": "<access_token>"
}
```

#### Success Response

Status: `200 OK`
```json
{}
```

#### Error Response

Status: `401 Unauthorized`
```json
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

---

## Tasks

### Task Field Validation

- **title**:
  - Required
  - Max 100 characters
- **description**:
  - Optional
  - Max 300 characters
- **priority**:
  - Required
  - Integer, must be 1 (low), 2 (medium), or 3 (high)
- **is_done**:
  - Boolean, default is `false`

#### Example Error Responses

**Title required**

Status: `400 Bad Request`
```json
{
  "title": ["This field is required."]
}
```

**Title too long**

Status: `400 Bad Request`
```json
{
  "title": ["Ensure this field has no more than 100 characters."]
}
```

**Description too long**

Status: `400 Bad Request`
```json
{
  "description": ["Ensure this field has no more than 300 characters."]
}
```

**Priority invalid value**

Status: `400 Bad Request`
```json
{
  "priority": ["Ensure this value is less than or equal to 3."]
}
```

---

### List & Create Tasks

- **GET** `/api/tasks/`
- **POST** `/api/tasks/`

#### List Tasks

**Filters (query params):**
- `priority` (1, 2, 3)
- `is_done` (true, false)
- `page` (default: 1)
- `size` (default: 10, max: 50)

**Request:**
```
GET /api/tasks/?priority=2&is_done=true&page=1&size=10
Authorization: Bearer <access_token>
```

**Success Response**

Status: `200 OK`
```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "title": "Task 1",
      "description": "Description",
      "priority": 2,
      "is_done": true,
      "created_at": "2025-09-30T12:00:00Z",
      "updated_at": "2025-09-30T12:00:00Z"
    }
  ]
}
```

**Error Response (unauthorized)**

Status: `401 Unauthorized`
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

#### Create Task

**Request:**
```json
{
  "title": "New Task",
  "description": "Details",
  "priority": 1
}
```
Authorization: Bearer <access_token>

**Success Response**

Status: `201 Created`
```json
{
  "id": 3,
  "title": "New Task",
  "description": "Details",
  "priority": 1
}
```

**Error Response (unauthorized)**

Status: `401 Unauthorized`
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

### Retrieve, Update & Delete Task

- **GET `/api/tasks/{id}/`**
- **PATCH `/api/tasks/{id}/`**
- **DELETE `/api/tasks/{id}/`**

**Authorization:** Bearer <access_token>

#### Retrieve

**Success Response**

Status: `200 OK`
```json
{
  "id": 1,
  "title": "Task Test 1",
  "description": "Task test description",
  "priority": 2,
  "is_done": false,
  "created_at": "2025-09-30T12:00:00Z",
  "updated_at": "2025-09-30T12:00:00Z"
}
```

**Error Response (not found)**

Status: `404 Not Found`
```json
{
  "detail": "No Task matches the given query."
}
```

**Error Response (unauthorized)**

Status: `401 Unauthorized`
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

#### Update

**Request:**
```json
{
  "title": "Updated Task",
  "priority": 1
}
```

**Success Response**

Status: `200 OK`
```json
{
  "id": 1,
  "title": "Updated Task",
  "description": "Task test description",
  "priority": 1,
  "is_done": false,
  "created_at": "2025-09-30T12:00:00Z",
  "updated_at": "2025-09-30T12:05:00Z"
}
```

**Error Response (not found)**

Status: `404 Not Found`
```json
{
  "detail": "No Task matches the given query."
}
```

**Error Response (unauthorized)**

Status: `401 Unauthorized`
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

#### Delete

**Success Response**

Status: `204 No Content`

**Error Response (not found)**

Status: `404 Not Found`
```json
{
  "detail": "No Task matches the given query."
}
```

**Error Response (unauthorized)**

Status: `401 Unauthorized`
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

## Requirements

- Python 3.8+
- Django & Django REST Framework
- PostgreSQL (production)

## Run

```bash
python manage.py migrate
python manage.py runserver
```

## Test 

```bash
python manage.py test 
```

## Deployed URL 

[Todo py API Deploy](https://todo-py-api.onrender.com)

---

## License

MIT – see [LICENSE](LICENSE)