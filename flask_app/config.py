# an extension targeted at Gunicorn deployments with an internal metrics endpoint
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics


def child_exit(server, worker):
    """Called just after a worker has been exited, in the master process.

        The callable needs to accept two instance variables for the Arbiter and
        the just-exited Worker.

    Args:
        server (_type_): _description_
        worker (_type_): _description_
    """
    GunicornInternalPrometheusMetrics.mark_process_dead_on_child_exit(worker.pid)
