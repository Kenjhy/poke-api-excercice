from dotenv import load_dotenv
import os

load_dotenv()

from fastapi import FastAPI
from app.controllers.berry_controller import router as berry_router


app = FastAPI()

app.include_router(berry_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv("API_HOST"), port=int(os.getenv("API_PORT")))