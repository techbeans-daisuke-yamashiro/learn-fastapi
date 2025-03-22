from core import app
from core import Settings
import uvicorn

# 設定オブジェクトを読み込み
settings = Settings()

if __name__ == "__main__":
    uvicorn.run(
        app="core:app",
        port=settings.fastapi_port,
        host=settings.fastapi_host,
        reload=settings.fastapi_reload
    )