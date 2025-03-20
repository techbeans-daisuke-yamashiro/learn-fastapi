from fastapi import FastAPI
from pydantic_settings import BaseSettings
from sqlmodel import create_engine, SQLModel, Session
from os import environ as env

app_root=env.get("APP_PROJECT","/app")

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

    class Config:
        extra = "ignore"
        env_file = f"{app_root}/.env"



#FastAPIのインスタンスを作成
app = FastAPI()


#設定を読み込み
settings=Setting()

#データベース接続を構成
databese_url=(
    f"{settings.db_driver}://{settings.db_user}:{settings.db_password}@"
    + f"{settings.db_host}:{settings.db_port}/{settings.db_name}")
engine = create_engine(databese_url, echo=settings.db_echo)

#SQLModelとデータベース接続を紐づけ
SQLModel.metadata.create_all(engine)

#DBセッションを生成
def get_session():
    with Session(engine) as session:
        yield session