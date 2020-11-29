#!/usr/bin/env bash
(cd survey_service; python manage.py createsuperuser)
(cd survey_service; gunicorn survey_service.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3) &
nginx -g "daemon off;"
