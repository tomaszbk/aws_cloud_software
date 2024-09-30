import boto3

from app.config import cfg

# Initialize a session using Amazon DynamoDB
dynamodb = boto3.resource("dynamodb", region_name=cfg.AWS_REGION)

products_table = dynamodb.Table("products")

users_table = dynamodb.Table("users")
