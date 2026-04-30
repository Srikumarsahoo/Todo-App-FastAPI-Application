# Todo App FastAPI Application

This project is a full-stack Todo application built with FastAPI, SQLAlchemy, Jinja2 templates, JWT authentication, and PostgreSQL. It provides both browser pages and REST API endpoints for creating accounts, logging in, managing personal todo items, updating user details, and giving admin users access to all todos.

## Main Application

The main purpose of this project is to demonstrate a production-style FastAPI backend with database configuration, authentication, authorization, HTML templates, and automated tests.

It can be used as:

- A personal task management application.
- A learning project for FastAPI routing, dependency injection, and SQLAlchemy ORM.
- A starter structure for apps that need user login, role-based permissions, database models, migrations, and tests.
- A reference for connecting FastAPI with PostgreSQL and testing with SQLite.

## Features

- User registration and login.
- JWT-based authentication.
- Cookie-based login flow for browser pages.
- Password hashing with bcrypt.
- Todo CRUD operations.
- User-specific todo access.
- Admin-only route to view and delete any todo.
- User profile endpoint.
- Password update endpoint.
- Phone number update endpoint.
- Jinja2 HTML pages for login, registration, adding todos, editing todos, and listing todos.
- Static assets served from the application.
- Alembic migration support.
- Pytest test suite using a separate SQLite test database.

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Jinja2 templates
- Passlib bcrypt
- Python JOSE JWT
- Pytest

## Project Structure

```text
TodoApp/
  main.py                 # FastAPI application entry point
  database.py             # Database engine, session, and Base configuration
  models.py               # Users and Todos SQLAlchemy models
  Routers/
    auth.py               # Register, login, token, and authentication helpers
    todos.py              # Todo pages and todo API endpoints
    users.py              # User profile, password, and phone update endpoints
    admin.py              # Admin-only todo endpoints
  templates/              # Jinja2 HTML templates
  static/                 # CSS and JavaScript assets
  alembic/                # Database migration files
  test/                   # Automated tests
```

## Database Configuration

The application currently uses PostgreSQL in `TodoApp/database.py`:

```python
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password@localhost/yourdatabasename'
```

Make sure PostgreSQL is running and the username, password, host, and database name match your local setup.

For SQLite development, the file also includes this example connection string:

```python
sqlite:///./todosapp.db
```

The tests use a separate SQLite database named `testdb.db`.

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell:

```bash
.\.venv\Scripts\Activate.ps1
```

Install the required packages:

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary alembic passlib[bcrypt] python-jose[cryptography] python-multipart pydantic[email] jinja2 pytest httpx
```

## Run the Application

Start the FastAPI development server:

```bash
uvicorn TodoApp.main:app --reload
```

Open the application in your browser:

```text
http://127.0.0.1:8000
```

The root URL redirects to:

```text
/todos/todo-page
```

API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Browser Pages

- `/auth/login-page` - Login page
- `/auth/register-page` - Registration page
- `/todos/todo-page` - Current user's todos
- `/todos/add-todo-page` - Add a new todo
- `/todos/edit-todo-page/{todo_id}` - Edit an existing todo

## API Endpoints

### Health

- `GET /healthy` - Check application health

### Authentication

- `POST /auth/` - Create a new user
- `POST /auth/token` - Login and receive a bearer token
- `POST /auth/login` - Login and store token in a cookie for browser usage

### Todos

- `GET /todos/` - Get all todos for the authenticated user
- `GET /todos/todo/{todo_id}` - Get one todo owned by the authenticated user
- `POST /todos/todo` - Create a todo
- `PUT /todos/todo/{todo_id}` - Update a todo
- `DELETE /todos/todo/{todo_id}` - Delete a todo

### Users

- `GET /user/` - Get the current user's profile
- `PUT /user/password` - Update the current user's password
- `PUT /user/phone_number/{phone_number}` - Update the current user's phone number

### Admin

- `GET /admin/todo` - Admin-only endpoint to get all todos
- `DELETE /admin/todo/{todo_id}` - Admin-only endpoint to delete any todo

## Todo Request Format

When creating or updating a todo, send data in this format:

```json
{
  "title": "Learn FastAPI",
  "description": "Practice routers, models, and authentication",
  "priority": 5,
  "complete": false
}
```

Validation rules:

- `title` must be at least 3 characters.
- `description` must be between 3 and 100 characters.
- `priority` must be between 1 and 5.
- `complete` must be true or false.

## Testing

Run the test suite with:

```bash
pytest TodoApp/test
```

The tests override the production database dependency and use SQLite, so they can run without writing to the PostgreSQL database.

## Performance Notes

The application is designed for efficient small-to-medium CRUD usage:

- FastAPI provides high-performance request handling.
- SQLAlchemy sessions are created per request and closed after use.
- JWT authentication keeps authentication stateless.
- Todo queries are scoped by `owner_id`, so users only load their own records.
- Primary keys are indexed by SQLAlchemy for fast lookup by ID.
- Admin routes are protected by role checks before database operations.

No benchmark results are included in this repository, so performance should be measured in your own deployment environment before using it for heavy production traffic.

## Security Notes

- Passwords are hashed before storage.
- JWT tokens expire after 20 minutes.
- Normal users can only access todos that belong to them.
- Admin routes require the authenticated user's role to be `admin`.

For production, move `SECRET_KEY` and database credentials into environment variables instead of keeping them in source code.

## Summary

This project is mainly a FastAPI database configuration and authentication practice application. It shows how to organize routers, models, templates, database sessions, migrations, authentication, authorization, and tests in one working Todo app.
