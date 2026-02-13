# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set working directory
ENV APP_HOME /app
WORKDIR $APP_HOME

# Removes output stream buffering, allowing for more efficient logging
ENV PYTHONUNBUFFERED 1

# Install system dependencies required for psycopg2-binary
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install pardner library (copied by CI into pardner-lib/)
COPY pardner-lib/ /tmp/pardner-lib/
RUN pip install --no-cache-dir /tmp/pardner-lib/ && \
    rm -rf /tmp/pardner-lib/

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy local code to the container image
COPY . .

# Collect static files for WhiteNoise (required since we don't use GCS)
RUN DJANGO_SECRET_KEY=build-placeholder python manage.py collectstatic --no-input

# Run the web service on container startup
# Cloud Run sets the PORT environment variable
# Gunicorn configuration:
# - capture-output: Capture stdout/stderr in logs
# - bind: Listen on all interfaces on the PORT provided by Cloud Run
# - workers: 1 worker process (Cloud Run handles scaling)
# - threads: 8 threads per worker (for handling concurrent requests)
# - timeout: 0 (no timeout, Cloud Run handles this)
CMD exec gunicorn --capture-output --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 pardnersite.wsgi
