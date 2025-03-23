from fastapi import FastAPI
from .settings import Settings
from routers import api_router

settings = Settings()

app = FastAPI()

app.include_router(api_router)

@app.get("/")
def root():
  return {"message":"hello from FastAPI"}