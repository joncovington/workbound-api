# workbound-api
A workflow management API

Before running docker-compose:
  create .env in the /app level with the environment variables shown in example.env
  docker-compose --env-file ./app/.env run app sh -c "python manage.py makemigrations"
  docker-compose --env-file ./app/.env run app sh -c "python manage.py migrate"

Don't forget to create your superuser!
docker-compose --env-file ./app/.env run --rm app sh -c "python manage.py createsuperuser"

Run container using:
  docker-compose --env-file ./app/.env up

Run tests using:
  docker-compose --env-file ./app/.env run app sh -c "python manage.py test && flake8"