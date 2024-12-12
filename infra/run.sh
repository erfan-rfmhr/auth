#!/bin/sh
python3 manage.py migrate && gunicorn config.wsgi --config config/gunicorn_config.py -b 0.0.0.0:8000