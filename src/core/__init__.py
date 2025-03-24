from models import setup_models
from routers import api_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "hello from FastAPI"}





