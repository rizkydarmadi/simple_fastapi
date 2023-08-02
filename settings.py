from pydantic import BaseModel


class Settings(BaseModel):
    secret_key: str
    sqlalchemy_url: str = (
        "postgresql+psycopg://postgres:12qwaszx@localhost:8000/postgres"
    )
    access_token_expire_minutes: int = (
        60 * 24 * 8
    )  # 60 minutes * 24 hours * 8 days = 8 days
    super_user_email: str = "admin@example.com"
    super_user_password: str = "12qwaszx"

    class Config:
        env_file = ".env"


settings = Settings()

if settings.super_user_password is None:
    settings.super_user_password = settings.secret_key
