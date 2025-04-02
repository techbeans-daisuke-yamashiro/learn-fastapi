from core.settings import Settings,emulator_ports
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
  
  def verify(self,token):
    headers = jwt.get_unverified_header(token)
    kid = headers.get("kid")

    # 公開鍵取得（エミュレータ or 本番 Firebase）
    certs_url = "http://firebase:9099/identitytoolkit.googleapis.com/keys"
    res = requests.get(certs_url)
    keys = res.json().get("keys", [])

    public_key = None
    for key in keys:
        if key["kid"] == kid:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
            break

    if not public_key:
        raise ValueError("Unable to find matching public key")

    try:
        decoded = jwt.decode(token, public_key, algorithms=["RS256"])
        return decoded  # UID は decoded['sub']
    except JWTError as e:
        raise ValueError(f"Token validation error: {str(e)}")

  def get_auth_endpoint(self,without_version=False):
    version = "/v1" if not without_version else ""
    url = f"https://identitytoolkit.googleapis.com/{version}"
    if self.__settings.firebase_emulator_host:
      url=(f"http://{self.__settings.firebase_emulator_host}"
           + f":{emulator_ports['auth']}/identitytoolkit.googleapis.com"
           + f"{version}")
    return url