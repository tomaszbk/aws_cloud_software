from app.database.dynamo_config import products_table, users_table
from app.database.models import Product, User


def insert_user(user: User):
    try:
        response = users_table.put_item(
            Item=user.model_dump(), ConditionExpression="attribute_not_exists(phone_number)"
        )
        print("Item inserted successfully:", response)
    except Exception as e:
        print("Unexpected error:", e)


def insert_product(product: Product):
    try:
        response = products_table.put_item(
            Item=product.model_dump(),
        )
        print("Item inserted successfully:", response)
    except Exception as e:
        print("Unexpected error:", e)


def add_purchase(user_phone_number: str, product: Product):
    try:
        response = users_table.update_item(
            Key={"phone_number": user_phone_number},
            UpdateExpression="SET purchases = list_append(if_not_exists(purchases, :empty_list), :new_purchase)",
            ExpressionAttributeValues={
                ":new_purchase": [product.model_dump()],  # New purchase as a single-element list
                ":empty_list": [],  # Empty list to initialize purchases if it doesn't exist
            },
        )
        message = f"Item inserted successfully: {response}, for product {product.product_id}, {product.name}"
        print(message)
        return message
    except Exception as e:
        message = f"Unexpected error: {e}"
        print(message)
        return message
