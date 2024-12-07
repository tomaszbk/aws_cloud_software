import uuid
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel


class User(BaseModel):
    phone_number: str
    name: str
    last_name: str | None = None
    email: str = None


class Category(str, Enum):
    tv = "tv"
    cellphone = "cellphone"
    laptop = "laptop"

class OrchestrationAction(str, Enum):
    NORMAL_CONVERSATION = "NORMAL_CONVERSATION"
    GET_PRODUCTS = "GET_PRODUCTS"
    PURCHASE = "PURCHASE"


class Product(BaseModel):
    product_id: str = str(uuid.uuid4())
    name: str
    price: Decimal
    description: str = None
    category: Category
    image_url: str = None
