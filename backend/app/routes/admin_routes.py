from app.auth import user_is_admin
from app.models import (
    Product,
    User,
    engine,
)
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

router = APIRouter()


templates = Jinja2Templates(directory="app/templates")


@router.get("/admin")
def index(request: Request, user: User = Depends(user_is_admin)):
    return templates.TemplateResponse("admin_index.html", {"request": request})


@router.get("/admin/product/list")
def products_view(request: Request, user: User = Depends(user_is_admin)):
    with Session(engine) as session:
        products = session.exec(select(Product)).all()
    return templates.TemplateResponse(
        "product_list.html", {"products": products, "request": request}
    )


@router.get("/admin/product/create")
def product_create_view(request: Request, user: User = Depends(user_is_admin)):
    return templates.TemplateResponse("product_create.html", {"request": request})


@router.post("/admin/product/create")
def product_create(
    request: Request,
    product_data: Product = Depends(),
    user: User = Depends(user_is_admin),
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


@router.get("/admin/product/update/{product_id}")
def product_update_view(
    request: Request, product_id: int, user: User = Depends(user_is_admin)
):
    with Session(engine) as session:
        product = session.get(Product, product_id)
    return templates.TemplateResponse(
        "product_update.html", {"request": request, "product": product}
    )


@router.post("/admin/product/update/{product_id}")
def product_update(
    request: Request,
    product_id: int,
    product_data: Product = Depends(),
    user: User = Depends(user_is_admin),
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


@router.post("/admin/product/delete/{product_id}")
def product_delete(
    request: Request, product_id: int, user: User = Depends(user_is_admin)
):
    with Session(engine) as session:
        product = session.get(Product, product_id)
        session.delete(product)
        session.commit()
    return RedirectResponse(
        url="/admin/product/list", status_code=status.HTTP_303_SEE_OTHER
    )


@router.get("/admin/user/list")
def users_view(request: Request, user: User = Depends(user_is_admin)):
    with Session(engine) as session:
        users = session.exec(select(User)).all()
    return templates.TemplateResponse(
        "user_list.html", {"users": users, "request": request}
    )


@router.get("/admin/user/create")
def user_create_view(request: Request, user: User = Depends(user_is_admin)):
    return templates.TemplateResponse("user_create.html", {"request": request})


@router.post("/admin/user/create")
def user_create(
    request: Request,
    user_data: User = Depends(),
    user: User = Depends(user_is_admin),
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


@router.get("/admin/user/update/{user_id}")
def user_update_view(
    request: Request, user_id: int, user: User = Depends(user_is_admin)
):
    with Session(engine) as session:
        user = session.get(User, user_id)
    return templates.TemplateResponse(
        "user_update.html", {"request": request, "user": user}
    )


@router.post("/admin/user/update/{user_id}")
def user_update(
    request: Request,
    user_id: int,
    user_data: User = Depends(),
    user: User = Depends(user_is_admin),
):
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
