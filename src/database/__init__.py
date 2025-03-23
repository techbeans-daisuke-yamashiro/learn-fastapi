from sqlmodel import create_engine,Session
from models import SQLModel, setup_models
import sqlalchemy as sa
from core.settings import Settings


def get_database_url(settings: Settings):
    return (
        f"{settings.db_driver}://{settings.db_user}:{settings.db_password}@"
        + f"{settings.db_host}:{settings.db_port}/{settings.db_name}?charset={settings.db_charset}"
    )


def get_engine(settings: Settings):
    return create_engine(get_database_url(settings=settings),echo=settings.db_echo) 


def get_model_by_tablename(table_name:str):
    for subclass in SQLModel.__subclasses__():
        if subclass.__tablename__ ==table_name:
            return subclass
    return None


def get_tablemames():
    return [s.__tablename__ for s in SQLModel.__subclasses__()]


settings = Settings()
engine = get_engine(settings=settings)


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
    
