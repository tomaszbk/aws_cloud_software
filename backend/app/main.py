import boto3
from fastapi import FastAPI, File, HTTPException, Request, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import cfg
from app.database.dynamo_get import get_products, get_user
from app.database.dynamo_insert import insert_product, insert_user
from app.database.models import Product, User
from app.send_event import send_event_to_eventbridge
from app.workflow import router as workflow_router

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(workflow_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == status.HTTP_303_SEE_OTHER:
        return exc.detail
    elif exc.status_code == status.HTTP_403_FORBIDDEN:
        return exc.detail
    elif exc.status_code == status.HTTP_400_BAD_REQUEST:
        return JSONResponse(exc.detail)


@app.post("/load-product")
async def load_product(
    name: str, description: str, price: float, category: str, image: UploadFile = File(...)
):
    s3 = boto3.client("s3")
    bucket = cfg.IMAGE_BUCKET_NAME
    s3.upload_fileobj(image.file, bucket, image.filename)
    image_url = f"https://{bucket}.s3.amazonaws.com/{image.filename}"
    product = Product(
        name=name, description=description, price=price, category=category, image_url=image_url
    )
    insert_product(product)
    return {
        "message": f"Product {product.name} loaded. image url: {product.image_url}. full product: {product}"
    }


@app.post("/load-user")
async def load_user(user: User):
    insert_user(user)
    return {"message": f"User {user.name} loaded. full user: {user}"}


@app.post("/send-email")
async def send_email(destiny_email: str, user_name: str):
    send_event_to_eventbridge(destiny_email, user_name)


@app.get("/get-products")
async def get_products_route(category: str):
    return get_products(category)


@app.get("/get-user")
async def get_user_route(phone_number: str):
    return get_user(phone_number)
