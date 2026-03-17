# Ledger Project

An open-source financial backend built with Django, Docker, and PostgreSQL.

## Setup

1. Clone the repo.
2. Create a `.env` file based on `.env.example`.
3. Run `docker compose up --build`.
4. Run migrations: `docker compose exec web python manage.py migrate`.
