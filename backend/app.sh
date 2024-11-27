#!/usr/bin/env sh

cd /app || exit 1

python manage.py makemigrations
python manage.py migrate

python manage.py runserver 0.0.0.0:8000