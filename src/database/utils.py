from models import SQLModel 
from sqlmodel import Session,create_engine
from core.settings import Settings

settings = Settings()
engine = create_engine(settings.get_database_url(), echo=settings.db_echo)


def get_model_by_tablename(table_name: str):
    for subclass in SQLModel.__subclasses__():
        if subclass.__tablename__ == table_name:
            return subclass
    return None


def get_tablenames():
    return [s.__tablename__ for s in SQLModel.__subclasses__()]

def get_session():
    with Session(engine) as session:
        yield session
