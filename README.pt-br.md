# todo-py-api

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2%2B-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14%2B-orange.svg)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13%2B-blue.svg)](https://www.postgresql.org/)
[![Licença: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Translation to en](README.md)

Uma API RESTful simples feita com Django para gerenciamento de tarefas pessoais, com autenticação JWT.

---


## Principais funcionalidades

- Sistema de usuários e autenticação JWT
- CRUD de tarefas (Criar, Ler, Atualizar, Deletar)
- Paginação e filtros para lista de tarefas
- Validação de campo com erros detalhados

---

## Tecnologias

- Python 3.8+
- Django 4.2+
- Django REST Framework 3.14+
- PostgreSQL (produção)

--- 

## Autenticação

### Validação dos campos do usuário

- **username**:
  - Obrigatório
  - Máximo 150 caracteres
  - Apenas letras, dígitos e caracteres `@/./+/-/_` permitidos
  - Único (não pode estar em uso)
- **password**:
  - Obrigatório
  - Máximo 128 caracteres
  - Sem restrições adicionais por padrão

#### Exemplos de respostas de erro

**Username muito longo**

Status: `400 Bad Request`
```json
{
  "username": ["Ensure this field has no more than 150 characters."]
}
```

**Username com caracteres inválidos**

Status: `400 Bad Request`
```json
{
  "username": ["Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters."]
}
```

**Username obrigatório**

Status: `400 Bad Request`
```json
{
  "username": ["This field is required."]
}
```

**Password obrigatório**

Status: `400 Bad Request`
```json
{
  "password": ["This field is required."]
}
```

**Password muito longo**

Status: `400 Bad Request`
```json
{
  "password": ["Ensure this field has no more than 128 characters."]
}
```

---

### Registrar

- **POST** `/api/auth/register/`

#### Requisição

```json
{
  "username": "newuser",
  "password": "newpassword"
}
```

#### Resposta de sucesso

Status: `201 Created`
```json
{
  "id": 1,
  "username": "newuser"
}
```

#### Resposta de erro

Status: `400 Bad Request`
```json
{
  "username": ["A user with that username already exists."]
}
```

---

### Login

- **POST** `/api/auth/login/`

#### Requisição

```json
{
  "username": "newuser",
  "password": "newpassword"
}
```

#### Resposta de sucesso

Status: `200 OK`
```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

#### Resposta de erro

Status: `401 Unauthorized`
```json
{
  "detail": "No active account found with the given credentials"
}
```

---

### Refresh de Token

- **POST** `/api/auth/token/refresh/`

#### Requisição

```json
{
  "refresh": "<refresh_token>"
}
```

#### Resposta de sucesso

Status: `200 OK`
```json
{
  "access": "<new_access_token>"
}
```

#### Resposta de erro

Status: `401 Unauthorized`
```json
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

---

### Verificar Token

- **POST** `/api/auth/token/verify/`

#### Requisição

```json
{
  "token": "<access_token>"
}
```

#### Resposta de sucesso

Status: `200 OK`
```json
{}
```

#### Resposta de erro

Status: `401 Unauthorized`
```json
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

---

## Tarefas

### Validação dos campos da tarefa

- **title**:
  - Obrigatório
  - Máximo 100 caracteres
- **description**:
  - Opcional
  - Máximo 300 caracteres
- **priority**:
  - Obrigatório
  - Inteiro, deve ser 1 (baixa), 2 (média) ou 3 (alta)
- **is_done**:
  - Booleano, padrão `false`

#### Exemplos de respostas de erro

**Título obrigatório**

Status: `400 Bad Request`
```json
{
  "title": ["This field is required."]
}
```

**Título muito longo**

Status: `400 Bad Request`
```json
{
  "title": ["Ensure this field has no more than 100 characters."]
}
```

**Descrição muito longa**

Status: `400 Bad Request`
```json
{
  "description": ["Ensure this field has no more than 300 characters."]
}
```

**Prioridade com valor inválido**

Status: `400 Bad Request`
```json
{
  "priority": ["Ensure this value is less than or equal to 3."]
}
```

---

### Listar & Criar Tarefas

- **GET** `/api/tasks/`
- **POST** `/api/tasks/`

#### Listar Tarefas

**Filtros (query params):**
- `priority` (1, 2, 3)
- `is_done` (true, false)
- `page` (default: 1)
- `size` (default: 10, max: 50)

**Exemplo de requisição:**
```
GET /api/tasks/?priority=2&is_done=true&page=1&size=10
Authorization: Bearer <access_token>
```

**Resposta de sucesso**

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

**Resposta de erro (não autenticado)**

Status: `401 Unauthorized`
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

#### Criar Tarefa

**Requisição:**
```json
{
  "title": "New Task",
  "description": "Details",
  "priority": 1
}
```
Authorization: Bearer <access_token>

**Resposta de sucesso**

Status: `201 Created`
```json
{
  "id": 3,
  "title": "New Task",
  "description": "Details",
  "priority": 1
}
```

**Resposta de erro (não autenticado)**

Status: `401 Unauthorized`
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

### Recuperar, Atualizar & Deletar Task

- **GET `/api/tasks/{id}/`**
- **PATCH `/api/tasks/{id}/`**
- **DELETE `/api/tasks/{id}/`**

**Authorization:** Bearer <access_token>

#### Recuperar

**Resposta de sucesso**

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

**Resposta de erro (não encontrado)**

Status: `404 Not Found`
```json
{
  "detail": "No Task matches the given query."
}
```

**Resposta de erro (não autenticado)**

Status: `401 Unauthorized`
```json
{
  "detail": "Authentication credentials were not provided."
}
```

#### Atualizar

**Requisição:**
```json
{
  "title": "Updated Task",
  "priority": 1
}
```

**Resposta de sucesso**

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

**Resposta de erro (não encontrado)**

Status: `404 Not Found`
```json
{
  "detail": "No Task matches the given query."
}
```

**Resposta de erro (não autenticado)**

Status: `401 Unauthorized`
```json
{
  "detail": "Authentication credentials were not provided."
}
```

#### Deletar

**Resposta de sucesso**

Status: `204 No Content`

**Resposta de erro (não encontrado)**

Status: `404 Not Found`
```json
{
  "detail": "No Task matches the given query."
}
```

**Resposta de erro (não autenticado)**

Status: `401 Unauthorized`
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

## Requisitos

- Python 3.8+
- Django & Django REST Framework
- PostgreSQL (produção)

## Rodar API

```bash
python manage.py migrate
python manage.py runserver
```

## Testar

```bash
python manage.py test 
```

## URL publico

[Todo py API Deploy](https://todo-py-api.onrender.com)

---

## Licença

MIT – veja [LICENÇA](LICENSE)
