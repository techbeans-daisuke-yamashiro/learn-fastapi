from fastapi import APIRouter
from schemas.auth import AuthrizationSchema
from core.settings import Settings

settings = Settings()

router = APIRouter(prefix="/auth")

@router.get('/')
def root():
  return {"detail":"auth top"}

@router.post("/login")
def login_user(user: AuthrizationSchema):
  return {"detail":"recrived"}