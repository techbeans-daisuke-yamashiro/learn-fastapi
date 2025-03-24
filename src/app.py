from core import app
from models import setup_models
from database.utils import engine
from core.settings import Settings
import uvicorn

# 設定オブジェクトを読み込み
settings = Settings()

if __name__ == "__main__":
    setup_models(engine)
    uvicorn.run(
        app="core:app",
        port=settings.fastapi_port,
        host=settings.fastapi_host,
        reload=settings.fastapi_reload
    )