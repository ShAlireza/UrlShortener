"""
pip install -r requirements.txt

a postgres database with blow credentials:

    DB_NAME='yektanet_interview'
    DB_USER='chitchat'
    DB_PASSWORD='chitchat'
    DB_HOST='localhost'
    DB_PORT='5432'

a local redis-server running on port 6379

commands:

    gunicorn --workers=4 --bind=0.0.0.0:8000 yektanet.wsgi:application
    celery -A yektanet beat -l info
    celery -A yektanet worker -l info

"""