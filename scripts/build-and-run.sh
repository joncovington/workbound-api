#!/usr/bin/env bash
# Build and run workbound-api with Nginx and PostgreSQL
set -ex

EXEC_CMD='docker-compose -f docker-compose.yml exec app'

docker-compose -f docker-compose.yml build

docker-compose -f docker-compose.yml up --detach

${EXEC_CMD} python manage.py test && flake8