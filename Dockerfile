# Dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Comando por defecto: aplica migraciones + arranca Gunicorn
CMD ["sh", "-c", \
     "python manage.py migrate --noinput && \
      python manage.py collectstatic --noinput && \
      gunicorn server.wsgi:application --bind 0.0.0.0:8081"]