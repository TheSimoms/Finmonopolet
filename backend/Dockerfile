# Backend
FROM python:3.8.0-alpine as dev

WORKDIR /app

# Install Postgres dependencies
RUN apk update \
    && apk --no-cache --virtual .build-dependencies add postgresql-dev gcc python3-dev musl-dev \
    && rm -rf .build-dependencies

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

# Install backend dependencies
RUN pip install --upgrade pip gunicorn
COPY requirements.txt .
RUN pip install -r requirements.txt

# Add project files
COPY src src

CMD ["python" ,"src/manage.py", "runserver", "0.0.0.0:8081"]

# Prod stage
FROM dev as prod

WORKDIR /app/src

CMD ["gunicorn", "finmonopolet.wsgi:application", "--workers=4", "--threads=4", "--bind", "0.0.0.0:8081"]
