import boto3
import os

ENV = os.getenv("ENV")

match ENV:
    case "dev":
        
    case "prod":
        region = os.getenv("REGION", "us-east-1")
        dynamodb = boto3.resource("dynamodb", region_name="us-west-2")
        users_table = dynamodb.Table("users")
        products_table = dynamodb.Table("products")