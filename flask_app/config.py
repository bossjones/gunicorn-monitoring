# from __future__ import annotations # FIXME: Is this the problem

# an extension targeted at Gunicorn deployments with an internal metrics endpoint
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics

import logging

from gunicorn import glogging

def child_exit(server, worker):
    """Called just after a worker has been exited, in the master process.

        The callable needs to accept two instance variables for the Arbiter and
        the just-exited Worker.

    Args:
        server (_type_): _description_
        worker (_type_): _description_
    """
    GunicornInternalPrometheusMetrics.mark_process_dead_on_child_exit(worker.pid)

# This is the path to the health check endpoint and should match what you
# defined in your Flask application.
#
# By default, requests to this endpoint will NOT be logged.
health_check = "/ping"
# Logging
# https://docs.gunicorn.org/en/stable/settings.html#accesslog
# accesslog = '-' to log to stdout
accesslog = "-"
# https://docs.gunicorn.org/en/stable/settings.html#access-log-format
# h - remote address
# l - '-'
# u - currently '-', may be user name in future
# t - date of the request
# r - status line (e.g. GET / HTTP/1.1)
# s - status
# b - response length or '-'
# f - referer
# a - user agent
# M - request duration in milliseconds
# {x-request-id}i - request id if provided
#
# Example:
# 127.0.0.1 - - [13/Mar/2024:15:08:18 -0700] "GET /v1/ask HTTP/1.1" 405 153 "-" "curl/8.4.0" "0" "-"
access_log_format = (
    '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" "%(M)s" "x-request-id: %({x-request-id}i)s"'
)
errorlog = "-"
# https://docs.gunicorn.org/en/stable/settings.html#loglevel
# gunicon log levels: debug, info, warning, error, critical
loglevel = "debug"


# class CustomGUnicornLogger(glogging.Logger):
#     """Custom logger for GUnicorn."""

#     def setup(self, cfg):
#         """Create logger and add custom filter."""
#         super().setup(cfg)
#         logger = logging.getLogger("gunicorn.access")
#         logger.addFilter(HealthCheckFilter())


# class HealthCheckFilter(logging.Filter):
#     """Custom filter for GUnicorn logger."""

#     def filter(self, record):
#         """Skip logging requests containing our healthcheck."""
#         return record.getMessage().find(health_check) == -1


# logger_class = CustomGUnicornLogger
