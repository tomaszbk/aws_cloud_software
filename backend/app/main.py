from app.models import (
    create_db_and_tables,
)
from app.routes.admin_routes import router as admin_router
from app.routes.auth_routes import router as auth_router
from app.routes.llm_routes import router as llm_router
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
create_db_and_tables()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(admin_router, tags=["admin"])
app.include_router(auth_router, tags=["auth"])
app.include_router(llm_router, tags=["llm"])


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == status.HTTP_303_SEE_OTHER:
        return exc.detail
    elif exc.status_code == status.HTTP_403_FORBIDDEN:
        return exc.detail
    elif exc.status_code == status.HTTP_400_BAD_REQUEST:
        return JSONResponse(exc.detail)
