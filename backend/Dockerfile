FROM python:3.9-slim

WORKDIR /app

# Install system utilities and PostgreSQL dev libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY . ./backend

# Compile Prisma client bindings inside container context
RUN prisma generate --schema=backend/prisma/schema.prisma

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
