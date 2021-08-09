#!/bin/sh

python manage.py migrate --noinput || exit 1
python manage.py init_admin || exit 1
python manage.py collectstatic --noinput || exit 1
gunicorn app.wsgi:application --bind 0.0.0.0:8000

exec "$@"