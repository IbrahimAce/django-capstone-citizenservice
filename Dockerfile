# Use an official lightweight Python image
FROM python:3.11-slim

# Prevent Python from writing .pyc files (keeps the container clean)
ENV PYTHONDONTWRITEBYTECODE=1

# Prevent Python from buffering stdout/stderr (logs appear immediately)
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first (Docker caches this layer — speeds up rebuilds)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project into the container
COPY . .

# Collect static files so they are served correctly in production
RUN python manage.py collectstatic --noinput

# Start the application using gunicorn (production-grade WSGI server)
# gunicorn replaces Django's development server (runserver) in production
# --workers 2 means 2 parallel worker processes
# TODO (April 16): Add Celery worker as a separate service in docker-compose
CMD ["gunicorn", "citizenservice.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
