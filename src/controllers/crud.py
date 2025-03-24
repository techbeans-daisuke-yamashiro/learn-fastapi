from sqlmodel import Session
from models import SQLModel
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse



def read_all(model,session:Session):
  data = model.select_all(session=session)
  status = 200
  if data==[]:
    data={"message":"not found"}
    status=404
  else:
    data = jsonable_encoder([d.as_dict() for d in data])
  return JSONResponse(content=data,status_code=status)


def read(model,id,session:Session):
  data = model.select_by_id(id=id,session=session)
  print(data)
  status = 200
  if data==None:
    data={"message":"not found"}
    status=404
  else:
    data=data.as_dict()
  return JSONResponse(content=jsonable_encoder(data),
  status_code=status)