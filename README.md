# workbound-api
A workflow management API

Before running docker-compose:
  create .env in the /app level with the environment variables shown in example.env

Run container using:
  docker-compose --env-file ./app/.env up

Run tests using:
  docker-compose --env-file ./app/.env run app sh -c "python manage.py test && flake8"