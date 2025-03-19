from fastapi import FastAPI
from pydantic_settings import BaseSettings


# .envをパース
class Setting(BaseSettings):
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


#FastAPIのインスタンスを作成
app = FastAPI()


#設定を読み込み
settings=Setting()