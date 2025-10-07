FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini .

EXPOSE 8000

#CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "2", "app.main:app", "-b", "0.0.0.0:8000"]
CMD ["gunicorn", "app.main:app", "--workers", "2", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker"]
