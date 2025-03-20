from core import app, settings
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        app="core:app"
    )