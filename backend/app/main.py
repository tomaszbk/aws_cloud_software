from fastapi import Depends, FastAPI, Form, Request, status
from fastapi.middleware.cors import CORSMiddleware

# import redirect
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from app.models import (
    Product,
    User,
    create_db_and_tables,
    engine,
)

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
create_db_and_tables()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/admin")
def index(request: Request):
    return templates.TemplateResponse("admin_index.html", {"request": request})


@app.get("/admin/product/list")
def products_view(request: Request):
    with Session(engine) as session:
        products = session.exec(select(Product)).all()
    return templates.TemplateResponse(
        "product_list.html", {"products": products, "request": request}
    )


@app.get("/admin/product/create")
def product_create_view(request: Request):
    return templates.TemplateResponse("product_create.html", {"request": request})


@app.post("/admin/product/create")
def product_create(
    request: Request,
    product_data: Product = Depends(),
):
    with Session(engine) as session:
        product = Product(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            stock=product_data.stock,
        )
        session.add(product)
        session.commit()
    return RedirectResponse(
        url="/admin/product/list", status_code=status.HTTP_303_SEE_OTHER
    )


@app.get("/admin/product/update/{product_id}")
def product_update_view(request: Request, product_id: int):
    with Session(engine) as session:
        product = session.get(Product, product_id)
    return templates.TemplateResponse(
        "product_update.html", {"request": request, "product": product}
    )


@app.post("/admin/product/update/{product_id}")
def product_update(
    request: Request,
    product_id: int,
    product_data: Product = Depends(),
):
    with Session(engine) as session:
        product = session.get(Product, product_id)
        product.name = product_data.name
        product.description = product_data.description
        product.price = product_data.price
        product.stock = product_data.stock
        session.add(product)
        session.commit()
    return RedirectResponse(
        url="/admin/product/list", status_code=status.HTTP_303_SEE_OTHER
    )


@app.post("/admin/product/delete/{product_id}")
def product_delete(request: Request, product_id: int):
    with Session(engine) as session:
        product = session.get(Product, product_id)
        session.delete(product)
        session.commit()
    return RedirectResponse(
        url="/admin/product/list", status_code=status.HTTP_303_SEE_OTHER
    )


@app.get("/admin/user/list")
def users_view(request: Request):
    with Session(engine) as session:
        users = session.exec(select(User)).all()
    return templates.TemplateResponse(
        "user_list.html", {"users": users, "request": request}
    )


@app.get("/admin/user/create")
def user_create_view(request: Request):
    return templates.TemplateResponse("user_create.html", {"request": request})


@app.post("/admin/user/create")
def user_create(
    request: Request,
    user_data: User = Depends(),
):
    with Session(engine) as session:
        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=user_data.hashed_password,
            is_admin=user_data.is_admin,
            is_active=user_data.is_active,
            phone=user_data.phone,
            name=user_data.name,
        )
        session.add(user)
        session.commit()
    return RedirectResponse(
        url="/admin/user/list", status_code=status.HTTP_303_SEE_OTHER
    )


@app.get("/admin/user/update/{user_id}")
def user_update_view(request: Request, user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
    return templates.TemplateResponse(
        "user_update.html", {"request": request, "user": user}
    )


@app.post("/admin/user/update/{user_id}")
def user_update(request: Request, user_id: int, user_data: User = Depends()):
    with Session(engine) as session:
        user = session.get(User, user_id)
        user.username = user_data.username
        user.email = user_data.email
        user.password = user_data.password
        session.add(user)
        session.commit()
    return RedirectResponse(
        url="/admin/user/list", status_code=status.HTTP_303_SEE_OTHER
    )
