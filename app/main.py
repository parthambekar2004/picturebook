from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router

app = FastAPI(title="PictureBook")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)
