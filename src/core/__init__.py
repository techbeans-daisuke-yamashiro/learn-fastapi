from models import setup_models
from routers import api_router
from fastapi import FastAPI,Depends
from dependencies.authorization import verify_api_key

app = FastAPI(dependencies=[Depends(verify_api_key)])

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "hello from FastAPI"}


