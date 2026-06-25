FROM node:20-alpine AS base

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy sources
COPY . .

# Set build variables
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production

# Compile application
RUN npm run build

EXPOSE 3000
ENV PORT=3000

CMD ["npm", "run", "start"]
