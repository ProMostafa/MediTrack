# Base image
FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y netcat-openbsd gcc postgresql libpq-dev

COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

COPY . /app/

RUN python manage.py migrate

EXPOSE 8000


CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "configuration.asgi:application"]
