from typing import List
from fastapi import APIRouter, Depends

from sqlmodel import Session
from database.utils import get_model_by_tablename,get_session
from controllers import crud

router=APIRouter(prefix='/item',
  tags=["Item"],
  description="アイテム管理")
Item= get_model_by_tablename('items')

@router.get('s', response_model=List[Item],description="全取得")
def all(session:Session = Depends(get_session)):
    return crud.read_all(model=Item,session=session) 


@router.get('/{id}', response_model=Item)
def read(id: int,session:Session = Depends(get_session)):
    return crud.read(model=Item,id=id,session=session)
