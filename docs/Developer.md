# Developer Setup Guide

Follow these steps to run Welth personal finance application locally.

## Prerequisite Tools
- Python 3.9+
- Node.js 18+ and npm
- Docker Desktop

## Backend Installation
1. Initialize virtual environment:
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Create environment variables in `backend/.env` (see template in `.env.example`).
3. Run Prisma client generation:
   ```bash
   PATH=./venv/bin:$PATH ./venv/bin/prisma generate --schema=prisma/schema.prisma
   ```

## Local Services via Docker
Start PostgreSQL and Redis:
```bash
docker compose up -d db redis
```

## Database Migrations & Seeding
Pushes the schema and seeds mock transactions, users, and holding assets:
```bash
PATH=./venv/bin:$PATH ./venv/bin/prisma db push --schema=prisma/schema.prisma
PYTHONPATH=. ./backend/venv/bin/python -m backend.app.core.seed
```

## Running Local Servers
- **Backend API Server**:
  ```bash
  cd backend
  source venv/bin/activate
  uvicorn backend.app.main:app --reload --port 8000
  ```
- **Celery Worker**:
  ```bash
  cd backend
  source venv/bin/activate
  celery -A backend.app.tasks.celery_app worker --loglevel=info
  ```
- **Frontend Server**:
  ```bash
  cd frontend
  npm install --legacy-peer-deps
  npm run dev
  ```
  Open `http://localhost:3000` to interact with Welth.
