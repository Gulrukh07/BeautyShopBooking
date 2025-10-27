#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies with uv
uv sync --frozen

# Collect static files
uv run python manage.py collectstatic --noinput

# Run migrations
uv run python manage.py migrate
