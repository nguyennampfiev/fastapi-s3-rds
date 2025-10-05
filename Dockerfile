# ===== Stage 1: Build dependencies =====
FROM python:3.13-slim AS builder

# Prevent Python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install build tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Install pdm/uv if needed to export requirements (optional)
# COPY pyproject.toml uv.lock /app/
# RUN pip install --upgrade pip pdm uv && uv export -f requirements > requirements.txt

# For now, let's assume you already have requirements.txt
COPY requirements.txt /app/

# Install dependencies into /install directory
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# ===== Stage 2: Runtime =====
FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy only installed packages from builder stage
COPY --from=builder /install /usr/local

# Copy application code
COPY app /app/app
COPY alembic /app/alembic
COPY alembic.ini /app/

EXPOSE 8000

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "app.main:app", "-b", "0.0.0.0:8000"]
