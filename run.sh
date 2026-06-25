#!/usr/bin/env bash

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
AMBER='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color
BOLD='\033[1m'

echo -e "${BLUE}${BOLD}====================================================${NC}"
echo -e "${BLUE}${BOLD}           Welth Platform Startup Script            ${NC}"
echo -e "${BLUE}${BOLD}====================================================${NC}"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}[ERROR] Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo -e "${RED}[ERROR] Docker daemon is not running. Please start Docker Desktop or the Docker daemon.${NC}"
    exit 1
fi

echo -e "${GREEN}[1/3] Spinning up Docker containers...${NC}"
docker compose up --build -d

if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR] Docker compose failed to bring up the services.${NC}"
    exit 1
fi

echo -e "${GREEN}[2/3] Waiting for database and backend services to become healthy...${NC}"
# Wait for backend container to be running and healthy
attempts=0
max_attempts=30
backend_ready=false

while [ $attempts -lt $max_attempts ]; do
    status=$(docker compose ps backend --format "{{.Status}}")
    if [[ "$status" == *"Up"* && "$status" != *"health: starting"* ]]; then
        backend_ready=true
        break
    fi
    echo -n "."
    sleep 2
    attempts=$((attempts + 1))
done
echo ""

if [ "$backend_ready" = false ]; then
    echo -e "${AMBER}[WARNING] Backend took too long to start. Skipping automatic database push. You may need to run it manually.${NC}"
else
    echo -e "${GREEN}[3/3] Running database schema sync via Prisma...${NC}"
    docker compose exec -T backend prisma db push --schema=backend/prisma/schema.prisma
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}[SUCCESS] Database schema is fully synced.${NC}"
    else
        echo -e "${AMBER}[WARNING] Database schema sync encountered an issue. Double-check backend logs.${NC}"
    fi
fi

echo -e "\n${BLUE}${BOLD}====================================================${NC}"
echo -e "${GREEN}${BOLD}🎉 Welth is up and running!${NC}"
echo -e "${BLUE}${BOLD}====================================================${NC}"
echo -e "${BOLD}Access the services here:${NC}"
echo -e "  - ${BOLD}Frontend Dashboard:${NC}  ${BLUE}http://localhost:3000${NC}"
echo -e "  - ${BOLD}Backend API Docs:${NC}    ${BLUE}http://localhost:8000/docs${NC}"
echo -e "  - ${BOLD}Metrics Interface:${NC}   ${BLUE}http://localhost:8000/metrics${NC}"
echo -e "${BLUE}${BOLD}====================================================${NC}"
echo -e "${BOLD}Helpful Commands:${NC}"
echo -e "  - View logs:         ${AMBER}docker compose logs -f${NC}"
echo -e "  - View service logs: ${AMBER}docker compose logs -f <service_name>${NC} (frontend|backend|celery_worker)"
echo -e "  - Stop services:     ${AMBER}docker compose down${NC}"
echo -e "${BLUE}${BOLD}====================================================${NC}"
