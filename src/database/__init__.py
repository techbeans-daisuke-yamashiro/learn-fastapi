from sqlmodel import create_engine,Session
from models import SQLModel as SQLModel_
import sqlalchemy as sa
from core.settings import Settings

settings = Settings()

database_url=(
    f"{settings.db_driver}://{settings.db_user}:{settings.db_password}@"
    + f"{settings.db_host}:{settings.db_port}/{settings.db_name}?charset={settings.db_charset}"
    )
engine = create_engine(database_url,echo=settings.db_echo)
session_ = sa.orm.sessionmaker(engine, class_=Session)


def get_session():
    with Session(engine) as session:
        yield session



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
        for sc in SQLModel_.__subclasses__():
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
    
