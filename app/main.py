from fastapi import FastAPI
from app.router.file_conversion import router as file_conversion_router

app = FastAPI()

app.include_router(file_conversion_router)

app.get("/status/")
async def status():
    return {"status": "File Conversion API is running."}

