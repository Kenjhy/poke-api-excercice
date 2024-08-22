from dotenv import load_dotenv
import os

# Try to load the environment variable from .env if the file exist
if os.path.exists(".env"):
    load_dotenv()

from fastapi import FastAPI
from app.controllers.berry_controller import router as berry_router

app = FastAPI()
app.include_router(berry_router)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)