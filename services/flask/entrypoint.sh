#!/bin/sh
set -e

export FLASK_APP=run.py  # Ensure FLASK_APP is correctly set

echo "Waiting for Database...."
while ! nc -z db 3306; do
  sleep 1
done
echo "Database is up!"

export FLASK_MIGRATING=1

# Initialize migrations if the directory doesn't exist
if [ ! -d "migrations" ]; then
  echo "Initializing migrations directory..."
  flask db init
fi

echo "Generating Migration Scripts..."
flask db migrate -m 'Auto Migration' || echo "No migrations generated."

echo "Applying migrations..."
flask db upgrade

unset FLASK_MIGRATING

echo "Starting the application..."
exec gunicorn -b 0.0.0.0:5000 "run:app"
