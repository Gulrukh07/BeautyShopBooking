FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /apps

# Copy all files
COPY . /apps

# Install dependencies from pyproject.toml or requirements.txt
RUN uv sync --frozen

# Expose Django port
EXPOSE 8000

# Collect static files at build time
RUN uv run python manage.py collectstatic --noinput

# Start Django server using Gunicorn
CMD ["uv", "run", "gunicorn", "your_project_name.wsgi:application", "--bind", "0.0.0.0:8000"]
