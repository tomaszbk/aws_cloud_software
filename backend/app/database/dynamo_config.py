import boto3

# Initialize a session using Amazon DynamoDB
dynamodb = boto3.resource("dynamodb", region_name="us-east-2")

products_table = dynamodb.Table("products")

users_table = dynamodb.Table("users")