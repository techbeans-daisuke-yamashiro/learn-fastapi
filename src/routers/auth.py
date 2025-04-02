from fastapi import APIRouter
from schemas.auth import AuthroizationSchema,idTokenResponse
from core.settings import Settings
from services.authenticate import Authenticate
import os

settings = Settings()
auth = Authenticate()

router = APIRouter(prefix="/auth",tags=["auth"])

@router.get('/')
def root():
  return {"detail":"auth top"}

@router.post("/login",response_model =idTokenResponse)
def login_user(user: AuthroizationSchema):
  return auth.sign_in(user=user)