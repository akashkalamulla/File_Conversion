from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from app.services.pdf_service import convert_pdf_to_jpg, convert_pdf_to_word, convert_pdf_to_excel, convert_pdf_to_ppt
from app.services.file_service import convert_file_to_pdf

router = APIRouter()

@router.post("/convert/{file_type}-to-pdf/")
async def file_to_pdf(file_type: str, file: UploadFile = File(...)):
    return await convert_file_to_pdf(file_type, file)

@router.post("/convert/pdf-to-jpg/")
async def pdf_to_jpg(file: UploadFile = File(...)):
    return await convert_pdf_to_jpg(file)

@router.post("/convert/pdf-to-word/")
async def pdf_to_word(file: UploadFile = File(...)):
    return await convert_pdf_to_word(file)

@router.post("/convert/pdf-to-excel/")
async def pdf_to_excel(file: UploadFile = File(...)):
    return await convert_pdf_to_excel(file)

@router.post("/convert/pdf-to-ppt/")
async def pdf_to_ppt(file: UploadFile = File(...)):
    return await convert_pdf_to_ppt(file)
