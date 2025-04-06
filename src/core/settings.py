from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache
from os import environ as env
from os import path
import yaml
from utils import DotDict


app_root = env.get("APP_ROOT", "/app")
app_env = env.get("APP_ENV","local")

# デフォルト値をロード
def load_defaults():
    cwd = path.dirname(__file__)
    with open(f"{cwd}/defaults.yaml") as yml:
        data = yaml.safe_load(yml)
    return DotDict(data)


# .envをパース
class Settings(BaseSettings):
    __d__: object = load_defaults()
    # FastAPI(Uvicorn)関連
    fastapi_port: int = Field(default=__d__.fastapi.port)
    fastapi_host: str = Field(default=__d__.fastapi.host)
    fastapi_reload: bool = Field(default=__d__.fastapi.reload)
    api_key: str|None = Field(default=__d__.fastapi.api_key)
    # DB関連
    db_driver: str = Field(default=__d__.database.driver)
    db_host: str = Field(default=__d__.database.host)
    db_port: str = Field(default=__d__.database.port)
    db_name: str = Field(default=__d__.database.name)
    db_user: str = Field(default=__d__.database.user)
    db_password: str = Field(default=__d__.database.password)
    db_echo: bool = Field(default=__d__.database.echo)
    db_charset: str = Field(default=__d__.database.charset)
    #firebase(GCP)関連
    firebase_emulator_host: str|None = Field(default=
                                             __d__.firebase.emulator_host)
    gcloud_project_id: str=Field(default=
                                 __d__.gcloud_project_id)
    firebase_api_key: str = Field(default=
                                  __d__.firebase.api_key)
    firebase_auth_domain: str = Field(default=
                                      __d__.firebase.auth_domain)
    firebase_storage_bucket: str = Field(default=
                                         __d__.firebase.storage_bucket)
    firebase_database_url: str = Field(default=
                                       __d__.firebase.database_url)
    firebase_messaging_sender_id: str = Field(default=
                                              __d__.firebase.database_url)
    firebase_app_id: str = Field(default=
                                 __d__.firebase.app_id)
    # 認証関連（リフレッシュトークン／ログアウト済みトークンの保管）
    refresh_token_store: str = Field(default=__d__.refresh_token_store) 
    revoked_token_store: str = Field(default=__d__.revoked_token_store)

    class Config:
        extra = "ignore"
        env_file = f"{app_root}/.env"


    def get_database_url(self):
        return (
            f"{self.db_driver}://{self.db_user}:{self.db_password}@"
            + f"{self.db_host}:{self.db_port}/{self.db_name}?charset={self.db_charset}"
        )
    
    def get_firebase_emulator_ports(self):
        d = self.__d__.firebase.emulator.ports
        return {'auth':d.aurh,
            'hosting ': d.hosting,
            'functions': d.function,
            'datababse': d.database,
            'firestore': d.firestore,
            'pubsub': d.pubsub,
            'storage': d.storage
            }
    
    def get_firebase_auth_config(self):
        project_id = self.__d__.gcloud_project_id
        u = self.__d__.firebase.urls
        return{
            "project_id": project_id,
            "audience": project_id,
            "algorithm": "RS256",
            "issuer": f"{u.issuer}{project_id}",
            "certs_url": u.certs
        }
    
    def get_firestore_config(self,environment:str):
        f_ = __d__.firebase
        e_ = __d__.firebase.emulastor
        cfg={
            "production":{
                "api_key":self.firebase_api_key,
                "refresh_url": f_.urls.refresh
            },
            "emulator":{
                "api_key":__d__.firebase.api_key,
                "refresh_url":
                f"http://{self.firebase_emulator_host}:{e_.ports.auth}/{e_.refresh}",

            }
        }
        return cfg.get(environment)


@lru_cache
def get_settings():
    return Settings()
