from sqlmodel import create_engine, SQLModel
from sqlmodel import Session
import sqlalchemy as sa
from .settings import settings
from models import ModelBase

databese_url=(
    f"{settings.db_driver}://{settings.db_user}:{settings.db_password}@"
    + f"{settings.db_host}:{settings.db_port}/{settings.db_name}")
engine = create_engine(databese_url, echo=settings.db_echo)
Session_ = sa.orm.sessionmaker(engine, class_=Session)

#SQLModelとデータベース接続を紐づけ
SQLModel.metadata.create_all(engine)

#DBセッションを生成
def get_session():
    with Session(engine) as session:
        yield session


