FROM python:3.9.10-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

# Needed for prometheus client
ENV PROMETHEUS_MULTIPROC_DIR /tmp
ENV prometheus_multiproc_dir /tmp

# CMD gunicorn -c config.py --bind=0.0.0.0:8000 --workers=6 -k aiohttp.worker.GunicornWebWorker --statsd-host=${STATSD_HOST}:${STATSD_PORT} --statsd-prefix=${APP_NAME} app:aioapp
CMD gunicorn -c config.py --bind=0.0.0.0:8000 --workers=6 --statsd-host=${STATSD_HOST}:${STATSD_PORT} --statsd-prefix=${APP_NAME} app:app
