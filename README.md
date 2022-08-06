python manage.py runserver
python -m celery -A config worker -l info
python -m celery -A config beat -l info
