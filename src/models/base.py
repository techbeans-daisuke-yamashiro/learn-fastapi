from datetime import datetime,timezone
from typing import Optional
from sqlmodel import SQLModel, Field, Session
import sqlalchemy as sa

class TimestampMixin(SQLModel):
    __abstract__ = True
    created_at: datetime = Field(default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    deleted_at: Optional[datetime] = Field(nullable=True)


class ModelBase(TimestampMixin):
    
    @classmethod
    def select_by_id(cls,session:Session,id:int):
        return session.query(cls).filter(cls.id==id).all()
  
    @classmethod
    def select_all(cls,session:Session):
        return session.query(cls).all()

    def as_dict(self):
        return {c.name: getattr(self,c.name) for c in self.__table__.columns}


