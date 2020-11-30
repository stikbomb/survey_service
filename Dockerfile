# Dockerfile

FROM python:3.7-buster

RUN apt-get update && apt-get install nginx -y --no-install-recommends
COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

# copy source and install dependencies
RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/pip_cache
RUN mkdir -p /opt/app/survey_service
COPY requirements-docker.txt start-server.sh /opt/app/
COPY .pip_cache /opt/app/pip_cache/
COPY survey_service /opt/app/survey_service/
WORKDIR /opt/app
RUN pip install -r requirements-docker.txt --cache-dir /opt/app/pip_cache
RUN cd survey_service && python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic
RUN chown -R www-data:www-data /opt/app

# start server
EXPOSE 8020
STOPSIGNAL SIGTERM
CMD ["/opt/app/start-server.sh"]