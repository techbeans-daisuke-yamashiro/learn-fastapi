from core.settings import Settings
from schemas.auth import AuthroizationSchema,RefreshedTokenSchema
from services.token import (lookup_refresh_token,
                            refresh_token_with_env,
                            store_refresh_token,
                            revoke_token)
from middlewares.authorization import verify_token
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
import requests, json

class Authenticate(object):
  s_ = Settings()
  

  def sign_in(self,user: AuthroizationSchema):
    environment_="emulator" if self.s_.firebase_emulator_host else "production"
    content={}
    status=200
    url = (f"{self.get_auth_endpoint()}/accounts:signInWithPassword?"
            f"key={self.s_.firebase_api_key}" )
    try:
      payload =json.dumps({
        "email":user.email,
        "password":user.password,
         "returnSecureToken": True
      })
      headers={"Content-Type": "application/json"}
      res = requests.post(url=url, headers=headers,data=payload)
      content=res.json()
      status=res.status_code
      store_refresh_token(uid=content["localId"],
                          token=content["refreshToken"],
                          environment=environment_)
      return JSONResponse(content=jsonable_encoder(content),status_code=status)
    except Exception as e:
      print(e)
      raise HTTPException(status_code=500,detail=jsonable_encoder(e))

  def revoke(self,user):
    uid=user["sub"]
    try:
      revoke_token(uid=user["sub"])
      return JSONResponse(status_code=200,content={"message":"Token revoked"})
    except Exception as e:
      raise HTTPException(status_code=500,detail=e)
  
  def get_auth_endpoint(self,without_version=False):
    e_=self.s_.get_firebase_emulator_ports()
    version = "/v1" if not without_version else ""
    url = f"https://identitytoolkit.googleapis.com/{version}"
    if self.s_.firebase_emulator_host:
      url=(f"http://{self.s_.firebase_emulator_host}"
           + f":{e_['auth']}/identitytoolkit.googleapis.com"
           + f"{version}")
    return url

  def refresh(self,refresh_token:str):
    data = lookup_refresh_token(refresh_token)
    if not data:
      return HTTPException(status_code=401,detail="Invalid refresh token")
    try:
      refreshed = refresh_token_with_env(refresh_token,data["environment"])
      print(f"refresh() got ->{refreshed}")
      return RefreshedTokenSchema(
        idToken=refreshed["id_token"],
        accessToken=refreshed["access_token"],
        refreshToken=refreshed["refresh_token"],
        expiresIn=refreshed["expires_in"])
    except Exception as e:
      return HTTPException(status_code=500,detail=jsonable_encoder(e))
      raise e 
