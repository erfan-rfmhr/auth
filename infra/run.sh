#!/bin/sh
python3 manage.py migrate && python3 manage.py collectstatic --noinput && gunicorn config.wsgi --workers=3 -b 0.0.0.0:8000
