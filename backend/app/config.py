from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AWS_REGION: str | None = "us-east-1"
    AWS_BEDROCK_REGION: str | None = None
    AWS_BEDROCK_MODEL: str | None = None
    IMAGE_BUCKET_NAME: str | None = "product-images-utn-frlp"
    DEBUG: str = "True"


cfg = Settings()
