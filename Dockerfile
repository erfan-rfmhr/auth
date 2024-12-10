# STAGE 1: Requirements Builder: create `requirements.txt` by poetry
FROM docker.arvancloud.ir/python:3.11 as requirements_builder

ENV PIP_DEFAULT_TIMEOUT=1000 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.8.3

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN pip install "poetry==$POETRY_VERSION" \
    && poetry install --no-root --no-ansi --no-interaction \
    && poetry export -f requirements.txt -o requirements.txt

# STAGE 2: Build
FROM docker.arvancloud.ir/python:3.11

RUN apt update && \
    apt install -y postgis python3-gdal gdal-bin libgdal-dev libproj-dev libgeos-dev libspatialite-dev \
     libspatialite7 libsqlite3-mod-spatialite spatialite-bin ffmpeg

WORKDIR /app/
COPY --from=requirements_builder /app/requirements.txt .

RUN pip install -r requirements.txt

COPY . /app/

CMD ["/bin/sh","-c", \
    "gunicorn config.wsgi --config config/gunicorn_config.py -b 0.0.0.0:8000" \
]
