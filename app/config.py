from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    database_url: str = Field("postgresql://postgres:postgres@localhost/sistema_dpm", alias="DATABASE_URL")
    SECRET_KEY: str = Field("your-secret-key-here-change-in-production", alias="SECRET_KEY")
    ALGORITHM: str = Field("HS256", alias="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    debug: bool = Field(False, alias="DEBUG")
    app_name: str = Field("Sistema Municipal", alias="APP_NAME")

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
