from fastapi import APIRouter, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from app.services.conversion_service import *
from app.utils.file_validation import validate_file_type

router = APIRouter()

SAVE_FOLDER = "converted_files"

@router.post("/process/")
async def process_conversion(
    file_type: str = Form(...),
    file: UploadFile = Form(...)
):
    """Converts an uploaded file, saves it in 'converted_files/', and returns a download link."""
    try:
        file_type = file_type.strip()  # Remove extra spaces
        validate_file_type(file_type, file)
        input_io = BytesIO(await file.read())  # Read file into memory

        conversion_functions = {
            "jpg-to-pdf": jpg_to_pdf,
            "word-to-pdf": word_to_pdf,
            "excel-to-pdf": excel_to_pdf,
            "ppt-to-pdf": ppt_to_pdf,
            "html-to-pdf": html_to_pdf,
            "pdf-to-jpg": pdf_to_jpg,
            "pdf-to-word": pdf_to_word,
            "pdf-to-ppt": pdf_to_ppt,
            "pdf-to-excel": pdf_to_excel,
        }

        if file_type not in conversion_functions:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_type}")

        saved_file_path = await conversion_functions[file_type](input_io)

        # Generate a download link
        download_url = f"http://127.0.0.1:8000/download/{os.path.basename(saved_file_path)}"

        return {"message": "File converted successfully", "download_url": download_url}

    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@router.get("/download/{filename}")
async def download_file(filename: str):
    """Allows users to download a previously converted file from 'converted_files/'."""
    file_path = os.path.join(SAVE_FOLDER, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path, filename=filename)
