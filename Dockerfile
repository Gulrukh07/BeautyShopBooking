FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /apps

COPY ./ /apps

RUN uv sync


CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
