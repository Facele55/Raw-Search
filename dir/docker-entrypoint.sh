#!/bin/bash

# Collect static files
echo "Collect static files"
python3 manage.py collectstatic --noinput

python3 manage.py makemigrations --noinput

# Apply database migrations
echo "Apply database migrations"
python3 manage.py migrate admin --database=users_db
python3 manage.py migrate sessions --database=users_db
python3 manage.py migrate admin_honeypot --database=users_db
python3 manage.py migrate users --database=users_db

python3 manage.py migrate core --database=search_db
python3 manage.py migrate feedback --database=feedback_db
python3 manage.py migrate crawler --database=crawler_db
python3 manage.py migrate analytics --database=analytics_db

# Start server
echo "Starting server"
python3 manage.py runserver 0.0.0.0:8000
