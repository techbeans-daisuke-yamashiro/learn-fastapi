from models import setup_models
from routers import api_router
from fastapi import FastAPI,Depends
from middlewares.authorization import verify_api_key, verify_token
from .settings import Settings

se=Settings()


app = FastAPI(
    # API_KEYの指定があればヘッダ認証を有効化
    dependencies=[Depends(verify_api_key)] if se.api_key else None
    )

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "hello from FastAPI"}

@app.get("/protected")
def protected(user: dict=Depends(verify_token)):
    return {"message": "hello from protected endpoint"}

