# aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 730335488407.dkr.ecr.us-east-1.amazonaws.com


curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"destiny_email": "tzubik@alu.frlp.utn.edu.ar", "destiny_name" : "Tomas", "product_image_url": "https://product-images-utn-frlp.s3.us-east-1.amazonaws.com/81d2d0dd-fd56-4468-98ec-50f38fc060a5.webp"}' -H "Content-Type: application/json"