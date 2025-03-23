from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from database import get_session, get_model_by_tablename
print("spawn item.py")
router=APIRouter(prefix='/item',tags=["Item"])
Item= get_model_by_tablename('items')

@router.get('s', response_model=List[Item])
def read_all(session:Session = Depends(get_session)):
    return Item.select_all(session=session)


@router.get('/{id}', response_model=Item)
def read_item(id: int,session:Session = Depends(get_session)):
    item=Item.select_by_id(id=id,session=session)
    if item == None:
        return {"message": "Not found"},404
    else:
        return item,200