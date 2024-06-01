from app.auth import authenticate_user, create_access_token, hash_password
from app.config import get_session
from app.models import User, UserCreate, UserLogin
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from loguru import logger

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/login")
async def login_view(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(user_data: UserLogin = Depends(), session=Depends(get_session)):
    user = authenticate_user(session, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(user.username)

    response = RedirectResponse(url="/admin", status_code=303)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response


@router.get("/signup")
async def signup_view(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@router.post("/signup")
async def register(form_data: UserCreate, session=Depends(get_session)):
    logger.info("starting user registration")
    form_data.hashed_password = hash_password(form_data.hashed_password)
    user = User(**form_data, is_admin=False, is_active=True)
    session.add(user)
    session.commit()
    logger.info(f"new user {user.username} created")
    return RedirectResponse(url="/login", status_code=303)
