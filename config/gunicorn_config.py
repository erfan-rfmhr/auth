import os


def get_workers_count():
    return int(os.getenv("GUNICORN_WORKERS", "1"))


workers = get_workers_count()
loglevel = "warning"
accesslog = "-"
errorlog = "-"
timeout = 30  # Worker timeout in seconds
keepalive = 5  # Keep-alive connections setting
graceful_timeout = 30  # Timeout for graceful workers restart
max_requests = 1000  # Restart workers after they process this many requests
max_requests_jitter = 50  # Add jitter to max_requests to avoid thundering herd

try:
    from psycogreen.gevent import patch_psycopg
    from gevent import monkey

    worker_class = "gevent"
    # this ensures forked processes are patched with gevent/gevent-psycopg2

    def do_post_fork(server, worker):
        monkey.patch_all()
        patch_psycopg()
        worker.log.info("Made Psycopg2 Green")

    post_fork = do_post_fork
except ImportError:
    pass
