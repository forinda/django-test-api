# Django Task API

A simple REST API for managing tasks and categories, built with Django and Django REST Framework.

## Requirements

- Python 3.12
- Pipenv

## Setup

```bash
# Install dependencies
pipenv install

# Run migrations
pipenv run python manage.py migrate

# Start the server
pipenv run python manage.py runserver
```

## API Endpoints

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/task/` | List all tasks |
| POST | `/api/v1/task/` | Create a task (multipart/form-data) |
| GET | `/api/v1/task/{id}/` | Retrieve a task |
| PUT | `/api/v1/task/{id}/` | Update a task |
| PATCH | `/api/v1/task/{id}/` | Partial update a task |
| DELETE | `/api/v1/task/{id}/` | Delete a task |

### Categories

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/category/` | List all categories (includes tasks) |
| POST | `/api/v1/category/` | Create a category |
| GET | `/api/v1/category/{id}/` | Retrieve a category (includes tasks) |
| PUT | `/api/v1/category/{id}/` | Update a category |
| PATCH | `/api/v1/category/{id}/` | Partial update a category |
| DELETE | `/api/v1/category/{id}/` | Delete a category |

## Documentation

- Swagger UI: [/api/docs/](http://localhost:8000/api/docs/)
- ReDoc: [/](http://localhost:8000/)
- OpenAPI Schema: [/api/schema/](http://localhost:8000/api/schema/)

## Task Fields

| Field | Type | Description |
|-------|------|-------------|
| title | string | Task title (max 200 chars) |
| description | string | Task description |
| completed | boolean | Completion status (default: false) |
| priority | string | `Low`, `Medium`, or `High` (default: Low) |
| category | integer | Category ID (nullable) |
| thumbnail | file | Image upload (optional) |
