web: gunicorn social.wsgi --log-file -
release: python manage.py makemigrations
release: python manage.py collectstatic
release: python manage.py migrate