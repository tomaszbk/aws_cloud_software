from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AWS_REGION: str = None
    AWS_PROFILE_NAME: str = None
    AWS_BEDROCK_MODEL: str = None
    AWS_ACCESS_KEY_ID: str = None
    AWS_SECRET_ACCESS_KEY: str = None
    DEBUG: bool = True


cfg = Settings()
