gunicorn --log-level=debug --preload --bind=0.0.0.0:8888 --capture-output --workers=3 --threads=3 mainsite.wsgi
