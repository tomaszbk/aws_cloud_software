from boto3.dynamodb.conditions import Attr

from app.database.dynamo_config import products_table, users_table
from app.database.models import Category, Product

def get_products(category: Category):
    """Returns the first 3 products from the products table."""
    response = products_table.scan(FilterExpression=Attr("category").eq(category))
    if not response["Items"]:
        return []
    return response["Items"][:3]


def get_product_details(product_id: str, category: Category) -> Product | str:
    """Returns the product with the given product id."""
    response = products_table.get_item(Key={"product_id": product_id, "category": category})
    if not response.get("Item"):
        return "Product not found"
    return Product.model_validate(response.get("Item"))


def get_user(phone_number: str):
    """Returns the user with the given phone number."""
    response = users_table.get_item(Key={"phone_number": phone_number})
    if not response.get("Item"):
        return "User not found"
    return response.get("Item")
