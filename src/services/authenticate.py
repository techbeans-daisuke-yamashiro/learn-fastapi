from core.settings import Settings
from schemas.auth import AuthroizationSchema
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
import requests,json

settings = Settings()



class Authenticate(object):
  __settings = Settings()

  def sign_in(self,user: AuthroizationSchema):
    content={}
    status=200
    url = (f"{self.get_auth_endpoint()}/accounts:signInWithPassword?"
            f"key={self.__settings.firebase_api_key}" )
    print(f"sign_in():tryng->{url}")
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
    except Exception as e:
      content=e
      status=500
    return JSONResponse(content=content,status_code=status)

  def revoke(self,token):
    pass
  
  def get_auth_endpoint(self,without_version=False):
    s_=self.__settings
    e_=s_.get_firebase_emulator_ports()
    version = "/v1" if not without_version else ""
    url = f"https://identitytoolkit.googleapis.com/{version}"
    if self.__settings.firebase_emulator_host:
      url=(f"http://{s_.firebase_emulator_host}"
           + f":{e_['auth']}/identitytoolkit.googleapis.com"
           + f"{version}")
    return url

  def refresh(self,refresh_token:str):
    pass