import uuid
from enum import Enum

from pydantic import UUID4, BaseModel


class User(BaseModel):
    phone_number: str
    name: str
    last_name: str
    email: str = None


class Category(str, Enum):
    tv = "tv"
    cellphone = "cellphone"
    laptop = "laptop"


class Product(BaseModel):
    id: UUID4 = uuid.uuid4()
    name: str
    price: float
    description: str = None
    category: Category
    image_url: str = None
