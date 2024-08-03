class Settings:
    secret_key: str = "secret"
    sqlalchemy_url: str = "postgresql+psycopg://myuser:12qwaszx@db:8000/test_code"
    access_token_expire_minutes: int = (
        60 * 24 * 8
    )  # 60 minutes * 24 hours * 8 days = 8 days
    super_user_email: str = "admin@example.com"
    super_user_password: str = "12qwaszx"
