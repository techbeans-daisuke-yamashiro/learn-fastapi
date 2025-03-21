from core import app, settings
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        app="core:app",
        port=settings.fastapi_port,
        host=settings.fastapi_host,
        reload=settings.fastapi_reload
    )