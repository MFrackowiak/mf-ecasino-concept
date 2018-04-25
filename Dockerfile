FROM python:3.6.2

ENV APP_DIR /app
WORKDIR $APP_DIR

COPY requirements.txt $APP_DIR/
RUN pip install -r requirements.txt

COPY requirements_deployment.txt $APP_DIR/
RUN pip install -r requirements_deployment.txt

COPY ./ecasino $APP_DIR/

RUN mkdir -p $APP_DIR/var/log

RUN python manage.py collectstatic --noinput --settings ecasino.settings_docker

ENTRYPOINT python manage.py migrate && \
    gunicorn ecasino.wsgi:application --workers 3 --timeout 120 --bind :8000
