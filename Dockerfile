FROM python:3.12-slim

RUN --mount=type=cache,target=/var/cache/apt \
    apt update && apt install -y \
    nodejs \
    npm \
    docker.io \
    && \
    npm install -g aws-cdk

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY requirements.txt requirements.txt

RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install -r requirements.txt --system

VOLUME [ "/root/.aws" ]

CMD ["cdk", "--version"]
