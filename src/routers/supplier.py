from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from database.utils import get_model_by_tablename,get_session
from controllers import crud
from fastapi import APIRouter

Supplier = get_model_by_tablename('suppliers')

router=APIRouter(prefix="/supplier",
  tags=["suppliers"])

@router.get('s',response_model=List[Supplier])
def all(session:Session = Depends(get_session)):
  return crud.read_all(model=Supplier,session=session) 

@router.get('/{id}',response_model=Supplier)
def read(id:int, session:Session = Depends(get_session)):
  return crud.read(model=Supplier,id=id,session=session)