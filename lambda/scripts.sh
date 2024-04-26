aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 730335488407.dkr.ecr.us-east-1.amazonaws.com


# TEST
docker run -d -p 9000:8080 \
--entrypoint /usr/local/bin/aws-lambda-rie \
lambda-mail-test ./main

curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'