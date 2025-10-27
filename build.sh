#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
uv sync --frozen

# Collect static files
uv run python manage.py collectstatic --noinput

# Run database migrations automatically
uv run python manage.py makemigrations --noinput || true
uv run python manage.py migrate --noinput
