# Stage 1: Build frontend
FROM node:20-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Stage 2: Python application
FROM python:3.12-slim
WORKDIR /app

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir .

# Copy application code
COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini ./

# Copy built frontend into static directory
COPY --from=frontend-build /app/src/mchome2/static/ ./src/mchome2/static/

# Install the package in editable mode so imports work
RUN pip install --no-cache-dir -e .

EXPOSE 8000

CMD ["uvicorn", "mchome2.main:app", "--host", "0.0.0.0", "--port", "8000"]
