from app.config import products_table, users_table

from database.models import Product, User


def check_duplicate_pk_error(error):
    return error.response["Error"]["Code"] == "ConditionalCheckFailedException"


def insert_user(user: User):
    try:
        response = users_table.put_item(
            Item=user.model_dump(),
            ConditionExpression="attribute_not_exists(phone_number)",
        )
        print("Item inserted successfully:", response)
    except Exception as e:
        try:
            if check_duplicate_pk_error(e):
                print("User already exists!")
        except:
            print("Unexpected error:", e)


def insert_product(product: Product):
    try:
        response = products_table.put_item(
            Item=product.model_dump(),
            ConditionExpression="attribute_not_exists(id)",
        )
        print("Item inserted successfully:", response)
    except Exception as e:
        try:
            if check_duplicate_pk_error(e):
                print("Product already exists!")
        except:
            print("Unexpected error:", e)
