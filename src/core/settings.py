from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache
from os import environ as env

app_root = env.get("APP_ROOT", "/app")

# .envをパース


class Settings(BaseSettings):
    # FastAPI(Uvicorn)関連
    fastapi_port: int = Field(default=8000)
    fastapi_host: str = Field(default="0.0.0.0")
    fastapi_reload: bool = Field(default=False)
    api_key: str|None = Field(default=None)
    app_root: str = Field(default="/app")
    # DB関連
    db_driver: str = Field(default="mysql")
    db_host: str = Field(default="mysql")
    db_port: str = Field(default="3306")
    db_name: str = Field(default="app_db")
    db_user: str = Field(default="fastapi")
    db_password: str = Field(default="fastapi")
    db_echo: bool = Field(default=True)
    db_charset: str = Field(default="utf8")
    #firebase(GCP)関連
    with_firebase_emulator: bool = Field(default=False)
    firebase_emulator_host: str|None = Field(default="firebase")

    class Config:
        extra = "ignore"
        env_file = f"{app_root}/.env"

    def get_database_url(self):
        return (
            f"{self.db_driver}://{self.db_user}:{self.db_password}@"
            + f"{self.db_host}:{self.db_port}/{self.db_name}?charset={self.db_charset}"
        )
    

@lru_cache
def get_settings():
    return Settings()
