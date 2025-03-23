from fastapi import APIRouter
from models import get_model_by_tablename
from database import session_
print("spawn item.py")
_session_=session_()
router=APIRouter(prefix='/item',tags=["Item"])
Item= get_model_by_tablename('items')

@router.get('s')
def read_all():
    s = session_()
    return Item.select_all(session=_session_)


@router.get('/{id}')
def read_item(id: int):
    item=Item.select_by_id(id=id,session=_session_)
    if item == None:
        return {"message": "Not found"},404
    else:
        return item,200