from pydantic_settings import BaseSettings
from os import environ as env

app_root=env.get("APP_PROJECT","/app")

# .envをパース
class Settings(BaseSettings):
    # FastAPI(Uvicorn)関連
    fastapi_port: int=8000
    fastapi_host: str = "0.0.0.0"
    fastapi_reload: bool = False
    # DB関連
    db_driver: str = "mysql"
    db_host: str = "mysql"
    db_port: str = "3306"
    db_name: str = "app_db"
    db_user: str = "fastapi"
    db_password: str = "fastapi"
    db_echo: bool = True
    db_charset: str = "utf8"

    class Config:
        extra = "ignore"
        env_file = f"{app_root}/.env"

settings = Settings()