from sqlmodel import SQLModel
from core.settings import Settings
from .base import Base
import importlib
import pkgutil
import pathlib

settings = Settings() 

# 現在のディレクトリをベースにする
package_dir = pathlib.Path(__file__).resolve().parent

# __init__.pyを除くすべてのモジュールを import
for (_, module_name, _) in pkgutil.iter_modules([str(package_dir)]):
    if module_name != "__init__":
        importlib.import_module(f"{__name__}.{module_name}")


def setup_models():
    # SQLModelとDBを接続する
    SQLModel.metadata.create_all(get_engine(settings))
    # SQLModelとモデルメタデータを接続しAlembicから管理できるようにする
    SQLModel.metadata=Base.metadata


