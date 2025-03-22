from fastapi import FastAPI
from .settings import Settings

settings = Settings()

app = FastAPI()
