# task-manager-backend

Task Manager API — FastAPI + SQLAlchemy (async) + PostgreSQL + Docker

## Features

- 🚀 **FastAPI** with async/await support
- 🗄️ **PostgreSQL** with SQLAlchemy 2.0 (async)
- 🔄 **Database migrations** with Alembic
- 🐳 **Docker** & Docker Compose ready
- 📊 **Pydantic v2** for validation
- 📦 **Poetry** for dependency management

## Installation

```bash
git clone <your-repo-url>
cd task-manager-backend
cp .env.template .env
docker compose up --build -d
```

## Setup

After installation, run database migrations:

```bash
docker compose exec api alembic upgrade head
```

## Usage

- **API:** <http://localhost:8001>
- **Swagger UI:** <http://localhost:8001/docs>
- **Database:** PostgreSQL on port 5433

> Note: Ports are configured in `.env` via `HOST_WEB_PORT` (default: 8001) and `HOST_DB_PORT` (default: 5433)

### Common Commands

```bash
# View logs
docker compose logs -f api

# Stop services
docker compose down

# Rebuild after code changes
docker compose up --build -d

# Access container shell
docker compose exec api bash

# Create new migration
docker compose exec api alembic revision --autogenerate -m "Description"
```

## Project Structure

```
├── src/app/          # Application code
│   ├── routers/      # API route handlers
│   ├── models.py     # SQLAlchemy models
│   ├── schemas.py    # Pydantic schemas
│   ├── crud.py       # Database operations
│   ├── auth.py       # Authentication logic
│   ├── config.py     # Configuration
│   ├── db.py         # Database setup
│   └── main.py       # FastAPI app
├── alembic/          # Database migrations
│   └── versions/     # Migration files
├── docker/           # Docker configuration
│   ├── Dockerfile
│   └── docker-compose.yml
└── pyproject.toml    # Poetry dependencies
```
