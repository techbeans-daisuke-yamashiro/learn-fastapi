from sqlmodel import SQLModel
from database import engine
from .base import Base
from .item import Item
from .supplier import Supplier

SQLModel.metadata.create_all(engine)
SQLModel.metadata=Base.metadata
