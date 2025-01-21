import mimetypes
from fastapi import UploadFile, HTTPException

ALLOWED_FORMATS = {
    "jpg-to-pdf": ["image/jpeg", "image/png"],
    "word-to-pdf": ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"],
    "excel-to-pdf": ["application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
    "ppt-to-pdf": ["application/vnd.ms-powerpoint", "application/vnd.openxmlformats-officedocument.presentationml.presentation"],
    "html-to-pdf": ["text/html"],
    "pdf-to-jpg": ["application/pdf"],
    "pdf-to-word": ["application/pdf"],
    "pdf-to-ppt": ["application/pdf"],
    "pdf-to-excel": ["application/pdf"],
}

def validate_file_type(file_type: str, file: UploadFile):
    mime_type, _ = mimetypes.guess_type(file.filename)
    if not mime_type or mime_type not in ALLOWED_FORMATS.get(file_type, []):
        raise HTTPException(status_code=400, detail=f"Invalid file format: {file.filename}. Expected format: {ALLOWED_FORMATS[file_type]}")
