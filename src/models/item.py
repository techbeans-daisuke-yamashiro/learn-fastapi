from .base import ModelBase, TimestampMixin
from typing import Optional
from sqlmodel import Field 


class Item(ModelBase, TimestampMixin, table=True):
    __tablename__="items"
    __table_args__ = {'extend_existing': True} 
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=True)
    price: int = Field(nullable=True)
