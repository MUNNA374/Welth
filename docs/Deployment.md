# Deployment Guide

This document outlines deployment pipelines for deploying Welth in production.

## Docker Containers
Build and run the entire ecosystem locally or in server instances:
```bash
docker compose up -d --build
```

## Frontend Deploy (Vercel)
The Next.js 15 app is built for seamless deployment on Vercel:
1. Connect GitHub repository to Vercel.
2. Define environment variable `NEXT_PUBLIC_API_URL` pointing to your hosted FastAPI endpoint (e.g. `https://api.welth.com/api/v1`).
3. Deploy branch `main`.

## Backend Deploy (Railway / Render / AWS)
FastAPI can be easily deployed via Railway:
1. Create a service linking the `./backend` directory (with `Dockerfile`).
2. Bind environmental variables:
   - `DATABASE_URL` (production PostgreSQL connection string)
   - `REDIS_URL` (production Redis caching string)
   - `GEMINI_API_KEY` (Gemini API token)
   - `SECRET_KEY` (highly secure JWT key)
