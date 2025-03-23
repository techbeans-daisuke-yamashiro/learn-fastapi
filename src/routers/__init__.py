import importlib
import pkgutil
import pathlib
import inspect
from fastapi import APIRouter

api_router= APIRouter(prefix='/api')

# 現在のディレクトリをベースにする
package_dir = pathlib.Path(__file__).resolve().parent

# 現在のディレクトリ（api）をベースに走査
package_dir = pathlib.Path(__file__).resolve().parent
package_name = __name__  # "app.api" のようなパッケージ名

# __init__.py を除くすべてのモジュールを対象にする
for (_, module_name, _) in pkgutil.iter_modules([str(package_dir)]):
    if module_name == "__init__":
        continue

    # モジュールをインポート（例: app.api.users）
    module = importlib.import_module(f"{package_name}.{module_name}")

    # router という名前の APIRouter インスタンスがあるか探す
    router = getattr(module, "router", None)
    if isinstance(router, APIRouter):
       api_router.include_router(router)