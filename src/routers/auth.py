from fastapi import APIRouter,Depends
from schemas.auth import (
  AuthroizationSchema,
  idTokenResponse,
  VerifyTokenShchema,
  RefreshTokenSchema,
  LogoutSchema)
from core.settings import Settings
from services.authenticate import Authenticate
from middlewares.authorization import verify_token
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

@router.post("/logout")
def logout_user(cred:LogoutSchema,user: dict=Depends(verify_token)):
  print(f"logout_user(): got cred={cred} u={user}")
  return auth.revoke(user=user)

@router.post("/refresh")
def refresh_token(t:RefreshTokenSchema):
  return auth.refresh(refresh_token=t.refresh_token)

