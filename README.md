# Welth — AI-Powered Personal Finance Platform

Welth is a premium, enterprise-grade personal finance software platform. It aggregates checking accounts, credit cards, investment portfolios, outstanding loans, insurance policies, and billing schedules. It infuses Google Gemini AI OCR for parsing receipts, conversational financial advisors, and XGBoost Machine Learning models for predicting overspending and daily budget breaches.

## Key Features
- **Consolidated Net Worth**: Tracking checking balances, stock/crypto portfolios, and outstanding debt.
- **AI Receipt Scanner (OCR)**: Multimodal receipt upload parsing via Google Gemini.
- **XGBoost Forecasting**: Lag-based time-series predictions of tomorrow's spending.
- **Sliding-Window Rate Limiting**: Redis-backed protection schemas against API floods.
- **Double-Submit CSRF Protections**: Validating state mutations on React frontend and FastAPI gateway.
- **Prometheus & Sentry**: Live metrics monitoring and centralized error capturing.

## Tech Stack
- **Frontend**: React 19, Next.js 15, TypeScript, Tailwind CSS, Recharts, Framer Motion
- **Backend**: Python, FastAPI, Celery, Redis, Pydantic, Prisma ORM
- **Database**: PostgreSQL (Dockerized)
- **AI/ML**: Google Gemini AI, XGBoost, Scikit-learn

## Directory Structure
```
welth/
├── docker-compose.yml
├── .env.example
├── README.md
├── docs/ (Complete documentation markdown files)
├── backend/
│   ├── app/
│   │   ├── gateway.py (API Gateway layer)
│   │   ├── main.py (App entrypoint)
│   │   ├── controllers/ (API routers)
│   │   ├── services/ (Business logic & external fetchers)
│   │   ├── repositories/ (Type-safe Prisma CRUD)
│   │   ├── finance/ (Isolated finance calculations)
│   │   ├── ai/ (Gemini configuration & markdown prompts)
│   │   ├── ml/ (XGBoost training & inference pipeline)
│   │   ├── notifications/ (SMTP, SMS, Push adapters)
│   │   └── tasks/ (Celery workers for OCR and reminders)
│   ├── prisma/ (schema.prisma configuration)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/ (Dashboard, login, register, and chatbot pages)
│   │   ├── components/ (Sidebar and glass widgets)
│   │   └── lib/ (Axios client with CSRF injector)
│   └── package.json
└── tests/ (Unit, integration, and api test cases)
```

## Quick Start (Local Services via Docker)

1. **Clone and Configure**:
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   Add your `GEMINI_API_KEY` into `.env`.

2. **Spin Up PostgreSQL and Redis**:
   ```bash
   docker compose up -d db redis
   ```

3. **Install Backend Dependencies**:
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Sync Schema & Seed Database**:
   ```bash
   PATH=./venv/bin:$PATH ./venv/bin/prisma db push --schema=prisma/schema.prisma
   PYTHONPATH=. ./venv/bin/python -m backend.app.core.seed
   ```

5. **Run Development Servers**:
   - **Backend FastAPI API**:
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
   - **Frontend App**:
     ```bash
     cd frontend
     npm install --legacy-peer-deps
     npm run dev
     ```

6. Open `http://localhost:3000` to explore the dashboard. Use credentials `user@welth.com` / `UserPassword123` to log in.

## Automated Verification Tests
Run the test suite using:
```bash
PYTHONPATH=. ./backend/venv/bin/pytest
```
All tests verify finance math formulas, token sanitizations, and health metrics endpoints.
