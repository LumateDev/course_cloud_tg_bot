from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SSL_CERT_PATH: str

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
