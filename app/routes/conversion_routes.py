from io import BytesIO

from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse
from app.services.conversion_service import (
    jpg_to_pdf,
    word_to_pdf,
    encode_io_to_base64,
    excel_to_pdf,
    ppt_to_pdf,
    html_to_pdf,
    pdf_to_jpg,
    pdf_to_word,
    pdf_to_ppt,
    pdf_to_excel,
)

router = APIRouter()

@router.post("/process/")
async def process_conversion(file_type: str, file: UploadFile):
    """
    Handles file conversion based on the file type and uploaded file.
    """
    try:
        input_io = BytesIO(await file.read())

        if file_type == "jpg-to-pdf":
            output_io = await jpg_to_pdf(input_io)
        elif file_type == "word-to-pdf":
            output_io = await word_to_pdf(input_io)
        elif file_type == "excel-to-pdf":
            output_io = await excel_to_pdf(input_io)
        elif file_type == "ppt-to-pdf":
            output_io = await ppt_to_pdf(input_io)
        elif file_type == "html-to-pdf":
            output_io = await html_to_pdf(input_io)
        elif file_type == "pdf-to-jpg":
            output_files = await pdf_to_jpg(input_io)
            return JSONResponse(content={"output_files": output_files})
        elif file_type == "pdf-to-word":
            output_io = await pdf_to_word(input_io)
        elif file_type == "pdf-to-ppt":
            output_io = await pdf_to_ppt(input_io)
        elif file_type == "pdf-to-excel":
            output_io = await pdf_to_excel(input_io)
        else:
            return JSONResponse(content={"error": f"Unsupported file type: {file_type}"}, status_code=400)

        return JSONResponse(content={"file": encode_io_to_base64(output_io)})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
