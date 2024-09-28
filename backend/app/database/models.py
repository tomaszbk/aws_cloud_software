import uuid

from pydantic import UUID4, BaseModel


class User(BaseModel):
    phone_number: str
    name: str
    last_name: str
    email: str


class Product(BaseModel):
    id: UUID4 = uuid.uuid4()
    name: str
    price: float
    description: str
    category: str
    image_url: str
