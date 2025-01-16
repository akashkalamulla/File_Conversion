from fastapi import FastAPI
from app.routes.conversion_routes import router as conversion_router

app = FastAPI()

app.include_router(conversion_router, prefix="/conversion")
