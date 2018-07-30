web: gunicorn app:server --log-file=-
worker: celery -A tasks worker --loglevel=info
worker: celery -A tasks beat --loglevel=info
