from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AWS_REGION: str | None = None
    AWS_BEDROCK_REGION: str | None = None
    AWS_BEDROCK_MODEL: str | None = None
    DEBUG: str = "True"


cfg = Settings()
