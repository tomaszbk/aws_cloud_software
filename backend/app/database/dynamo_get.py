import boto3

from app.database.dynamo_config import products_table, users_table


def get_products(category: str):
    """Returns the first 3 products from the products table."""
    response = products_table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key("Category").eq(category)
    )
    return response["Items"][:3]


def get_product_details(product_id: str):
    """Returns the product with the given product id."""
    response = products_table.get_item(Key={"product_id": product_id})
    return response.get("Item")


def get_user(phone_number: str):
    """Returns the user with the given phone number."""
    response = users_table.get_item(Key={"phone_number": phone_number})
    return response.get("Item")
