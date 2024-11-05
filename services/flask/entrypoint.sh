#!/bin/sh

# Wait for the database to be ready.
echo "Waiting for Database...."

# Loop until the database is available
while ! nc -z db 3306; do
  sleep 1
done

echo "Database is up!"

# Generate Flask-Migrate migration scripts for database
echo "Generating Migration Scripts..."
flask db migrate -m 'Auto Migration'

# Apply migrations
echo "Applying migrations..."
flask db upgrade

# Execute the command passed to the container
exec "$@"

