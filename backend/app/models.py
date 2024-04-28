from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel, create_engine

engine = create_engine("sqlite:///test.db", connect_args={"check_same_thread": False})


class Prompt(BaseModel):
    content: str


# SQL MODEL
class Product(SQLModel, table=True):
    __tablename__ = "products"
    id: int = Field(primary_key=True)
    name: str
    description: str
    price: float
    stock: bool


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True)
    name: str
    email: str
    hashed_password: str
    is_admin: bool

    orders: list["Order"] = Relationship(back_populates="user")


class Order(SQLModel, table=True):
    __tablename__ = "orders"

    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    order_date: str
    quantity: int
    total: float

    order_details: list["OrderDetail"] = Relationship(back_populates="order")
    user: User = Relationship(back_populates="orders")


class OrderDetail(SQLModel, table=True):
    __tablename__ = "order_details"

    id: int = Field(primary_key=True)
    order_id: int = Field(foreign_key="orders.id")
    product_id: int = Field(foreign_key="products.id")
    quantity: int
    total: float

    product: Product = Relationship()
    order: Order = Relationship(back_populates="order_details")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
