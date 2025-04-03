from pydantic import BaseModel, Field, EmailStr

class AuthroizationSchema(BaseModel):
  email: EmailStr=Field()
  password: str=Field()

class idTokenResponse(BaseModel):
  kind:str
  registered: bool
  localId: str
  email: str
  idToken: str
  refreshToken: str
  expiresIn: str

class VerifyTokenShchema(BaseModel):
  token: str

class RefreshTokenSchema(BaseModel):
  refresh_token: str