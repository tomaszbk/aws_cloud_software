FROM alpine

RUN apk -v --no-cache --update add \
        nodejs \
        npm \
        python3 \
        ca-certificates \
        groff \
        less \
        bash \
        docker \
        make \
        curl \
        wget \
        zip \
        git \
        py-pip \
        && \
    update-ca-certificates && \
    npm install -g aws-cdk

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt --break-system-packages

VOLUME [ "/root/.aws" ]

CMD ["cdk", "--version"]