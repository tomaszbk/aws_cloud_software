# aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 730335488407.dkr.ecr.us-east-1.amazonaws.com


curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"destiny_email": "eluna@alu.frlp.utn.edu.ar"}'