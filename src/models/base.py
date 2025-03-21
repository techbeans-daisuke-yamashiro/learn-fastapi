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


# 論理削除フィルターを定義
@sa.event.listens_for(Session, "do_orm_execute")
def _add_filtering_deleted_at(execute_state):
    """
    論理削除用のfilterを自動的に適用する
    以下のようにすると、論理削除済のデータも含めて取得可能
    query(...).filter(...).execution_options(include_deleted=True)
    """
    if (
        execute_state.is_select
        and not execute_state.is_column_load
        and not execute_state.is_relationship_load
        and not execute_state.execution_options.get("include_deleted", False)
    ):
        for sc in SQLModel.__subclasses__():
            print(sc.__dir__())
            if hasattr(sc, "__table__") and hasattr(sc, "deleted_at"):
                execute_state.statement = execute_state.statement.options(
                    sa.orm.with_loader_criteria(
                        sc,
                        lambda cls: cls.deleted_at.is_(None),
                        include_aliases=True,
                    )
                )
    else:
        return