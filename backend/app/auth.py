from datetime import timedelta

import jwt
from app.config import get_session
from app.models import User
from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from passlib.context import CryptContext
from sqlmodel import Session, select

app = FastAPI()

# Configuration for JWT
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "e64b1149d445998de645136b902ebfc5e84411f58cfa1e1e0859258b514e4910"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def jwt_cookie_authorizer(request: Request, session=Depends(get_session)):
    # Extract token from cookies
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(303, RedirectResponse(url="/admin/login"))

    try:
        # Decode the JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise Exception("Invalid token data")
        query = select(User).where(User.username == username)
        user = session.exec(query).one_or_none()
        if user is None:
            raise Exception("User not found")
    except jwt.JWTError:
        raise HTTPException(303, RedirectResponse(url="/admin/login"))

    return user


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(session: Session, username, password: str):
    query = select(User).where(User.username == username)
    user = session.exec(query).one_or_none()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str):
    access_token_expires = timedelta(minutes=60)
    to_encode = {"sub": username, "exp": access_token_expires}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def user_is_admin(user: User = Depends(jwt_cookie_authorizer)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail=RedirectResponse(url="/forbidden"))
    return user
