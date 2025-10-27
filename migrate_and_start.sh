#!/usr/bin/env bash
set -o errexit

echo "Waiting for database to be ready..."
until uv run python -c "import psycopg2; psycopg2.connect('${DATABASE_URL}')" > /dev/null 2>&1; do
  echo "Database unavailable, sleeping..."
  sleep 3
done

echo "Database ready — running migrations"
uv run python manage.py migrate --noinput

echo "Starting server..."
uv run gunicorn root.wsgi:application
