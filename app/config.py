from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    database_url: str = Field(..., alias="DATABASE_URL")
    secret_key: str = Field(..., alias="SECRET_KEY")
    debug: bool = Field(False, alias="DEBUG")
    app_name: str = Field("Sistema Municipal", alias="APP_NAME")

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
