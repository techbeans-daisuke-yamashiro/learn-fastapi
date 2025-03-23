from sqlmodel import SQLModel
from database import engine
from .base import Base
import importlib
import pkgutil
import pathlib


# 現在のディレクトリをベースにする
package_dir = pathlib.Path(__file__).resolve().parent

# __init__.pyを除くすべてのモジュールを import
for (_, module_name, _) in pkgutil.iter_modules([str(package_dir)]):
    if module_name != "__init__":
        importlib.import_module(f"{__name__}.{module_name}")

# SQLModelとDBを接続する
SQLModel.metadata.create_all(engine)
# SQLModelとモデルメタデータを接続しAlembicから管理できるようにする
SQLModel.metadata=Base.metadata


def get_model_by_tablename(table_name:str):
    for subclass in SQLModel.__subclasses__():
        if subclass.__tablename__ ==table_name:
            return subclass
    return None


def get_tablemames():
    return [s.__tablename__ for s in SQLModel.__subclasses__()]