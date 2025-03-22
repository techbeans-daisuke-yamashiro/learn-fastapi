from typing import Optional
from sqlmodel import SQLModel,Field
from .mixin import TimestampMixin,ModelBaseMixin
from .base import Base

class Supplier(SQLModel, TimestampMixin,ModelBaseMixin,table=True):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "suppliers"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    address: str = Field(nullable=False)
    country: str = Field(default="JP",nullable=False)

