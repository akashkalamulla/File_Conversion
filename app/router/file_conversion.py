from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from app.services.file_service import process_conversion


router = APIRouter()

@router.post("/convert/")
async def convert_file(request: Request):
    """
    Converts files based on the provided input data.
    Input should include:
    - file_type: Type of file to convert (e.g., jpg-to-pdf, pdf-to-word).
    - file_content: Base64-encoded content of the file.
    """
    try:
        # Parse the input JSON
        body = await request.json()
        file_type = body.get("file_type")
        file_content = body.get("file_content")

        if not file_type or not file_content:
            raise HTTPException(status_code=400, detail="Missing file_type or file_content in request body.")

        # Process the file conversion
        result = await process_conversion(file_type, file_content)

        # Return the conversion result
        return JSONResponse(status_code=200,content={"status": "success", "result": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")