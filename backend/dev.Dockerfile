FROM python:3.12

ENV UV_SYSTEM_PYTHON=1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Change the working directory to the `code` directory
WORKDIR /code/backend
