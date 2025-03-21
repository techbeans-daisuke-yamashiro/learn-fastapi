from fastapi import Depends,APIRouter
from sqlmodel import Session
from core.database import get_session
from models import Item

item_router=APIRouter(prefix='/item')

@item_router.get('s')
def get_all(*, session:Session = Depends(get_session)):
    return [item.as_dict() for item in Item.select_all(session)]


@item_router.get('/{id}')
def get_item(*, session:Session = Depends(get_session), id:int):
    return session.get(Item,id)