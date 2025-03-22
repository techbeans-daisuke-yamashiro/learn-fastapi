from typing import Optional
from sqlmodel import SQLModel,Field
from .mixin import TimestampMixin,ModelBaseMixin
from .base import Base

SQLModel.metadata=Base.metadata

class Item(SQLModel, TimestampMixin,ModelBaseMixin,table=True):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "items"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=True)
    price: float= Field(nullable=True)
    currency: str= Field(default="JPY", nullable=False)

