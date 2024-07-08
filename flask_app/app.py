import logging
import random
import time

from flask import Flask, Response
from flask import Flask, Response, request
# an extension targeted at Gunicorn deployments with an internal metrics endpoint
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics
from aiohttp import web
from aiohttp_wsgi import WSGIHandler

app = Flask(__name__)


# enable flask metrics
metrics = GunicornInternalPrometheusMetrics(app, path="/metrics", export_defaults=True)

# static information as metric
metrics.info("app_info", "Application info", version="1.0.3")



@app.route("/")
def hello_world():
    app.logger.error("Hello, World!")
    return "Hello, World!"


@app.route("/io_task")
def io_task():
    time.sleep(2)
    return "IO bound task finish!"


@app.route("/cpu_task")
def cpu_task():
    for i in range(10000):
        n = i*i*i
    return "CPU bound task finish!"


@app.route("/random_sleep")
def random_sleep():
    time.sleep(random.randint(0, 5))
    return "random sleep"


@app.route("/random_status")
def random_status():
    status_code = random.choice([200] * 6 + [300, 400, 400, 500])
    return Response("random status", status=status_code)

def make_aiohttp_app(app):
    wsgi_handler = WSGIHandler(app)
    aioapp = web.Application()
    aioapp.router.add_route('*', '/{path_info:.*}', wsgi_handler)
    return aioapp

aioapp = make_aiohttp_app(app)

if __name__ != '__main__':
    # Use gunicorn's logger to replace flask's default logger
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
