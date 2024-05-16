#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput
echo "Collect static files finished...."

# Apply database migrations
echo "Starting Apply database migrations"
python manage.py migrate
echo "Apply database migrations finished...."

# Run management command
echo "Running create super user command"
python manage.py createsu
echo "Running create super user command finished...."

# Start server
echo "Starting server"
python3 manage.py runserver 0.0.0.0:8000
echo "Server started successfully...."

