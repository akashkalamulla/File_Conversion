from fastapi import APIRouter, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO
from app.services.conversion_service import *
from app.utils.file_validation import validate_file_type

router = APIRouter()


@router.post("/process/")
async def process_conversion(
        file_type: str = Form(...),
        file: UploadFile = Form(...)
):
    """Converts an uploaded file and returns it as a downloadable file."""
    try:
        file_type = file_type.strip()  # Remove extra spaces
        validate_file_type(file_type, file)

        input_io = BytesIO(await file.read())

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

        output_io = await conversion_functions[file_type](input_io)

        output_extension = {
            "jpg-to-pdf": "pdf",
            "word-to-pdf": "pdf",
            "excel-to-pdf": "pdf",
            "ppt-to-pdf": "pdf",
            "html-to-pdf": "pdf",
            "pdf-to-jpg": "jpg",
            "pdf-to-word": "docx",
            "pdf-to-ppt": "pptx",
            "pdf-to-excel": "xlsx",
        }

        output_filename = f"converted_file.{output_extension[file_type]}"
        content_type = {
            "pdf": "application/pdf",
            "jpg": "image/jpeg",
            "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        }.get(output_extension[file_type], "application/octet-stream")

        return StreamingResponse(
            output_io,
            media_type=content_type,
            headers={"Content-Disposition": f"attachment; filename={output_filename}"}
        )

    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
