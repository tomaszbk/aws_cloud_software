import boto3
from fastapi import FastAPI, File, HTTPException, Request, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.database.models import Product
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
async def load_product(name: str, description: str, price: float, image: UploadFile = File(...)):
    s3 = boto3.client("s3")
    bucket = "product-images-utn-frlp"
    s3.upload_fileobj(image.file, bucket, image.filename)
    image_url = f"https://{bucket}.s3.amazonaws.com/{image.filename}"
    product = Product(name=name, description=description, price=price, image_url=image_url)

    return {"message": f"Product {product.name} loaded. image url: {product.image_url}"}


@app.post("/send-email")
async def send_email(destiny_email: str):
    send_event_to_eventbridge(destiny_email)
