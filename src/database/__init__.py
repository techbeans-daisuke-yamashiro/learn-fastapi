from sqlmodel import create_engine, Session
from models import SQLModel
import sqlalchemy as sa
from core.settings import Settings





# 論理削除フィルタを定義
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
        # モデルクラスを検索し、フィルタを適用
        for sc in SQLModel.__subclasses__():
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
