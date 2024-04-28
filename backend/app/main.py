from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette_admin.contrib.sqla import Admin, ModelView

from app.models import (
    Product,
    User,
    create_db_and_tables,
    engine,
)

app = FastAPI()

create_db_and_tables()
admin = Admin(engine, title="Example: SQLAlchemy")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

admin.add_view(ModelView(User))
admin.add_view(ModelView(Product))

admin.mount_to(app)
