#!/usr/bin/env bash
set -o errexit

# Run migrations
uv run python manage.py migrate --noinput

# Start Django app
uv run gunicorn root.wsgi:application
