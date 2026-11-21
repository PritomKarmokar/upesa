# Upesa: Digital Wallet Backend

A Django REST Framework backend for digital wallet user management, authentication, and wallet provisioning.

> **Project Status:** Upesa is under active development. APIs, data models, and configuration may change without notice, and the project is not yet recommended for production use.

## Features

- Mobile-number-based registration for customers, agents, and merchants
- JWT authentication with token invalidation on login and logout
- Failed-login tracking with temporary account lockout
- Wallet creation (customer, agent float, merchant) in BDT or USD
- Database-enforced constraints: one wallet per user/type/currency and non-negative balances
- Correlation-ID-aware structured logging
- Django admin and Docker Compose setup

## Tech Stack

Python 3.12 · Django 5.2 · Django REST Framework · PostgreSQL 17 · Docker

## Getting Started

### With Docker

```bash
cp .env.example .env
docker compose up --build
```

Set `POSTGRES_DB_HOST=postgres_db` in `.env` when using Docker Compose. Migrations run automatically on startup.

### Without Docker

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # update the PostgreSQL values for your local instance
python manage.py migrate
python manage.py runserver
```

The API is served at `http://localhost:8000/<SERVICE_NAME>/api/v1/` (for example, `http://localhost:8000/upesa/api/v1/`).

## API Reference

| Method | Endpoint         | Auth | Description                          |
|--------|------------------|:----:|--------------------------------------|
| POST   | `/create-user/`  | No   | Register a wallet user               |
| POST   | `/user/login/`   | No   | Authenticate and obtain JWT tokens   |
| POST   | `/user/logout/`  | Yes  | Invalidate the user's current tokens |
| POST   | `/create-wallet/`| Yes  | Create a wallet for an active user   |

### Create User

```http
POST /upesa/api/v1/create-user/
Content-Type: application/json

{
  "username": "Jane Doe",
  "mobile_no": "+8801712345678",
  "user_type": "customer",
  "password": "StrongPass123",
  "confirm_password": "StrongPass123"
}
```

- Username: at least 4 characters
- Password: at least 8 characters
- Mobile number: valid and unique Bangladesh number; `+88`, `88`, and local formats are normalized

### Login

```http
POST /upesa/api/v1/user/login/
Content-Type: application/json

{
  "mobile_no": "01712345678",
  "password": "StrongPass123"
}
```

Returns access and refresh tokens with expiry information. After the configured number of consecutive failed attempts, the account is locked for the configured duration.

### Create Wallet

```http
POST /upesa/api/v1/create-wallet/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "user_id": "01KEXAMPLEULID",
  "wallet_type": "customer"
}
```

### Logout

```http
POST /upesa/api/v1/user/logout/
Authorization: Bearer <access_token>
```

## Authentication

Tokens are issued by Simple JWT (access: 5 minutes, refresh: 1 day by default). A token is accepted only if the user exists and is active, and the token's `token_version` claim matches the user's current version in the database. Both login and logout increment this version, so previously issued tokens are invalidated.

## Configuration

Copy `.env.example` to `.env` and adjust as needed.

| Variable                       | Description                                  | Example            |
|--------------------------------|----------------------------------------------|--------------------|
| `SERVICE_NAME`                 | URL prefix for the API                       | `upesa`            |
| `SECRET_KEY`                   | Django secret key                            | *(long random string)* |
| `DEBUG`                        | Enable debug mode                            | `True`             |
| `ALLOWED_HOSTS`                | Allowed host names                           | `127.0.0.1,localhost` |
| `CSRF_TRUSTED_ORIGINS`         | Trusted origins                              | `http://localhost` |
| `POSTGRES_DB_NAME`             | Database name                                | `upesa_db`         |
| `POSTGRES_DB_USER`             | Database user                                | `postgres`         |
| `POSTGRES_DB_PASSWORD`         | Database password                            | `postgres`         |
| `POSTGRES_DB_HOST`             | Database host                                | `localhost`        |
| `POSTGRES_DB_PORT`             | Database port                                | `5432`             |
| `MAX_FAILED_LOGIN_ATTEMPTS`    | Failed attempts before lockout               | `5`                |
| `LOCK_DURATION_TILL_MINUTES`   | Lockout duration in minutes                  | `30`               |
| `LOG_LEVEL`                    | Logging level                                | `DEBUG`            |

## Project Structure

```text
upesa/      Project settings and root URL configuration
wallets/    Models, serializers, views, authentication, and admin
applibs/    Shared utilities (auth, choices, logging, validation, responses)
```

## Development

```bash
python manage.py check             # system checks
python manage.py test              # run tests
python manage.py createsuperuser   # admin access at /<SERVICE_NAME>/admin/
```

Make targets are also available: `make run`, `make migrations`, `make migrate`.

## Production Checklist

- Set `DEBUG=False` and restrict `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`
- Use a unique `SECRET_KEY` and strong database credentials
- Replace Django's development server with Gunicorn
- Serve behind a reverse proxy with TLS
- Configure database backups, rate limiting, and centralized logging
