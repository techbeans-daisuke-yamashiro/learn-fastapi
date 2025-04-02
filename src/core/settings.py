from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache
from os import environ as env

app_root = env.get("APP_ROOT", "/app")
app_env = env.get("aPP_ENV","local")
emulator_ports={
    'auth': 9099,
    'hosting ': 500,
    'functions': 5001,
    'datababse': 9000,
    'firestore': 8080,
    'pubsub': 8085,
    'storage': 9199
}


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
    firebase_emulator_host: str|None = Field(default=None)
    gcloud_project_id: str=Field(default="example")
    firebase_api_key: str = Field(default="fake-api-key")
    firebase_auth_domain: str = Field(default="localhost")
    firebase_storage_bucket: str = Field(default="localhost")
    firebase_database_url: str = Field(default="demo-project.appspot.com")
    firebase_messaging_sender_id: str = Field(default="1234567890")
    firebase_app_id: str = Field(default="1:1234567890:web:abcdefghijklmnopqrstuvwxyz)")

    class Config:
        extra = "ignore"
        env_file = f"{app_root}/.env"


    def get_database_url(self):
        return (
            f"{self.db_driver}://{self.db_user}:{self.db_password}@"
            + f"{self.db_host}:{self.db_port}/{self.db_name}?charset={self.db_charset}"
        )
    
    def get_firebase_endpoints(self):
        return {
            "apiKey": self.firebase_api_key,
            "authDomain": self.firebase_auth_domain,
            "databaseURL": self.firebase_database_url,
            "projectId": self.gcloud_project_id,
            "storageBucket": self.firebase_storage_bucket,
            "messagingSenderId": self.firebase_messaging_sender_id,
            "appId": self.firebase_app_id
        }


@lru_cache
def get_settings():
    return Settings()
