import logging
import os
from fastapi import FastAPI
from app.routes.conversion_routes import router as conversion_router
from prometheus_fastapi_instrumentator import Instrumentator

# Ensure the logs directory exists
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)  # Create the logs directory if it doesn't exist

# Logging Configuration
logging.basicConfig(level=logging.INFO, filename=LOG_FILE, filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# FastAPI App
app = FastAPI(title="File Conversion API", description="Convert files between formats.", version="1.0")

# Include Routes
app.include_router(conversion_router, prefix="/conversion")

# Enable API Monitoring
Instrumentator().instrument(app).expose(app)

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "File Conversion API is running"}
