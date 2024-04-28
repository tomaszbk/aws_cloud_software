from datetime import date

from pydantic import BaseModel
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

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
    username: str
    phone: str
    name: str
    email: str
    hashed_password: str
    is_admin: bool
    is_active: bool


def get_user_by_username(username: str):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == username)).first()
        return user


def add_user(
    username: str,
    phone: str,
    name: str,
    email: str,
    hashed_password: str,
    is_admin: bool,
    is_active: bool,
):
    with Session(engine) as session:
        user = User(
            username=username,
            phone=phone,
            name=name,
            email=email,
            hashed_password=hashed_password,
            is_admin=is_admin,
            is_active=is_active,
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def create_db_and_tables():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
