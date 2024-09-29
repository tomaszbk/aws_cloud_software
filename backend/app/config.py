from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AWS_REGION: str | None = None
    AWS_BEDROCK_REGION: str | None
    AWS_PROFILE_NAME: str | None = None
    AWS_BEDROCK_MODEL: str | None = None
    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None
    DEBUG: bool = True


cfg = Settings()
