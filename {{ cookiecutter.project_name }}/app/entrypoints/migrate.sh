#!/bin/sh

while ! nc -z db 5432; do echo "Waiting for db:5432"; sleep 5; done
while ! echo 'SELECT 1' | PGPASSWORD=$POSTGRES_PASSWORD psql --host $POSTGRES_HOST --user $POSTGRES_USER $POSTGRES_DB; do echo "Waiting for DB"; sleep 5; done

python manage.py migrate || exit 1
echo "migrate finished successfully"
