from fastapi import APIRouter
from .item import item_router

api_router = APIRouter(prefix='/api')

api_router.include_router(item_router)

@api_router.get('/')
def root():
    return {"message":"hello from fastAPI"}