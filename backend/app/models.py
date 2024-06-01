from datetime import date

from app.pyd_form import as_form
from pydantic import BaseModel
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

engine = create_engine("sqlite:///test.db", connect_args={"check_same_thread": False})


class Prompt(BaseModel):
    content: str


# SQL MODEL
@as_form
class Product(SQLModel, table=True):
    __tablename__ = "products"
    id: int = Field(primary_key=True)
    name: str
    description: str
    price: float
    stock: int


@as_form
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True, default=None)
    username: str
    phone: str
    name: str
    last_name: str
    email: str
    hashed_password: str
    is_admin: bool
    is_active: bool


@as_form
class UserCreate(SQLModel, table=False):
    username: str
    phone: str
    name: str
    email: str
    hashed_password: str


@as_form
class UserLogin(SQLModel, table=False):
    username: str
    password: str


def get_user_by_username(username: str):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == username)).first()
        return user


def create_db_and_tables():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    product = Product(
        name="Phone",
        description="An awesome phone",
        price=299.99,
        stock=10,
    )
    with Session(engine) as session:
        session.add(product)
        session.commit()
        session.refresh(product)
