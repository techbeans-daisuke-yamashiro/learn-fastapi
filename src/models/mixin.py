from datetime import datetime,timezone
from typing import Optional
from sqlmodel import SQLModel, Field, Session
from sqlalchemy.ext.declarative import declared_attr
import sqlalchemy as sa


class TimestampMixin(object):

    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now,
                                 sa_column_kwargs={'onupdate': datetime.now},
                                 nullable=False)
    deleted_at: datetime = Field(nullable=True)


class ModelBaseMixin(object):
    __abstract__ = True
    
    @classmethod
    def select_by_id(cls,session:Session,id:int):
        return session.query(cls).filter(cls.id==id).all()
  
    @classmethod
    def select_all(cls,session:Session):
        return session.query(cls).all()

    def as_dict(self):
        return {c.name: getattr(self,c.name) for c in self.__table__.columns}


