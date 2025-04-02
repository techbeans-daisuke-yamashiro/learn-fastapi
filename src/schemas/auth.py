from pydantic import BaseModel, Field, EmailStr

class AuthrizationSchema(BaseModel):
  email: EmailStr=Field()
  password: str=Field()