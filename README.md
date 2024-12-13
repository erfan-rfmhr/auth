# Auth project
A simple otp handler project in Django.

## Installation with Docker

- Run docker compose `docker compose up -d`
- Open http://localhost:8080/api/schema/swagger-ui/

## Installation without Docker

- Install poetry `pip install poetry==1.8.3`
- Install dependencies `poetry install`
- Migrate database `python manage.py migrate`
- Collect statics `python manage.py collectstatic --noinput`
- Run server `python manage.py runserver`
- Open http://localhost:8000/api/schema/swagger-ui/

## Configuration
IF you intend to use this project as it is, it does not need any extra configuration!
But if you wanted to, follow the `.env.example` file and create a `.env` file in root directory,
or change settings from `./config/settings/components` directly.

## How to run tests?
`python manage.py test`

## How it works?

- Use Django as the main framework.
- Use Nginx as a proxy server.
- Use Redis to cache block users with a counter.

