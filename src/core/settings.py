from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache
from os import environ as env

app_root = env.get("APP_ROOT", "/app")
app_env = env.get("aPP_ENV","local")
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
    firebase_emulator_host: str|None = Field(default="firebase:9099")

    class Config:
        extra = "ignore"
        env_file = f"{app_root}/.env"

    def get_database_url(self):
        return (
            f"{self.db_driver}://{self.db_user}:{self.db_password}@"
            + f"{self.db_host}:{self.db_port}/{self.db_name}?charset={self.db_charset}"
        )
    
    def get_firebase_config(self):
        api_key = "fake-api-key"
        auth_domain = "localhoat"
        database_url = (self.firebase_database_url
                        if self.firebase_database_url
                        else "http://localhost:9000?ns=fake-db")
        project_id = (self.project_id
                      if self.project_id else "demo-project")
        storage_bucket =(self.firebase_storage_bucket
                         if self.firebase_storage_bucket
                         else "demo-project.appspot.com")
        message_sender_id= (self.message_sender_id 
                            if self.message_sender_id else"1234567890")
        app_id = ("1:1234567890:web:abcdefghijklmnopqrstuvwxyz)")
        return {
            "apiKey": api_key,
            "authDomain": auth_domain,
            "databaseURL": database_url,
            "projectId": "demo-project",
            "storageBucket": "demo-project.appspot.com",
            "messagingSenderId": "1234567890",
            "appId": "1:1234567890:web:abcdefghijklmnopqrstuvwxyz"
        }
        

@lru_cache
def get_settings():
    return Settings()
