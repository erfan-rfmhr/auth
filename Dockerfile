FROM docker.arvancloud.ir/python:3.11

ENV PIP_DEFAULT_TIMEOUT=1000 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.8.3

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN apt update

RUN pip install "poetry==$POETRY_VERSION"
RUN poetry install --no-root --no-ansi --no-interaction
RUN poetry export -f requirements.txt -o requirements.txt

WORKDIR /app/

RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8000

RUN chmod +x ./infra/run.sh

CMD ["/bin/sh","-c", \
    "gunicorn config.wsgi --config config/gunicorn_config.py -b 0.0.0.0:8000" \
]
