#!/usr/bin/env bash
# Build and run workbound-api with Nginx and PostgreSQL
set -ex

EXEC_CMD='docker-compose -f docker-compose.yml exec app'

docker-compose -f docker-compose.yml build

docker-compose -f docker-compose.yml up --detach

echo Wait for database to become available...
while ! ${EXEC_CMD} bash -c 'nc -z "db" "5432"'; do
  sleep 0.5
done
echo Database ready!


${EXEC_CMD} python manage.py test