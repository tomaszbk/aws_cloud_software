FROM python:3.12-alpine

RUN apk update && apk add --no-cache \
    nodejs \
    npm \
    docker-cli \
    docker-cli-buildx \
    bash \
    git \
    && \
    npm install -g aws-cdk

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY requirements.txt requirements.txt

RUN uv pip install -r requirements.txt --system

VOLUME [ "/root/.aws" ]

CMD ["cdk", "--version"]
