import os
from dotenv import load_dotenv

load_dotenv()

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "static/uploaded_files")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "static/converted_files")
