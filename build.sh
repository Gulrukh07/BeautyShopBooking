#!/usr/bin/env bash
set -o errexit

# Install dependencies
uv sync --frozen

# Collect static assets
uv run python manage.py collectstatic --noinput

# Apply migrations (do NOT create them here)
uv run python manage.py migrate --noinput
