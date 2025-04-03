from fastapi import APIRouter
from schemas.auth import (
  AuthroizationSchema,
  idTokenResponse,
  VerifyTokenShchema,
  RefreshTokenSchema)
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


@router.post("/refresh")
def refresh_token(t:RefreshTokenSchema):
  return auth.refresh(token=t.refresh_token)

