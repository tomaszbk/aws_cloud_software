from app.database.dynamo_config import products_table

def get_products(category: str):
    """Returns the first 3 products from the products table."""
    response = products_table.scan()
    return response["Items"][:3]