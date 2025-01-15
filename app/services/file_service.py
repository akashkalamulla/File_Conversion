import base64
import os
from pathlib import Path
from fpdf import FPDF
from PIL import Image
import img2pdf
from pdf2image import convert_from_path
from docx import Document
from pptx import Presentation
import pandas as pd
from PyPDF2 import PdfReader

UPLOAD_DIR = "static/uploaded_files"
OUTPUT_DIR = "static/converted_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def process_conversion(file_type: str, file_content: str):
    """
    Handles file conversion based on the file type and Base64-encoded content.
    """
    input_path = save_base64_file(file_content)
    output_path = generate_output_path(input_path, file_type)

    if file_type == "jpg-to-pdf":
        await jpg_to_pdf(input_path, output_path)
    elif file_type == "word-to-pdf":
        await word_to_pdf(input_path, output_path)
    elif file_type == "excel-to-pdf":
        await excel_to_pdf(input_path, output_path)
    elif file_type == "ppt-to-pdf":
        await ppt_to_pdf(input_path, output_path)
    elif file_type == "html-to-pdf":
        await html_to_pdf(input_path, output_path)
    elif file_type == "pdf-to-jpg":
        return await pdf_to_jpg(input_path)
    elif file_type == "pdf-to-word":
        await pdf_to_word(input_path, output_path)
    elif file_type == "pdf-to-ppt":
        await pdf_to_ppt(input_path, output_path)
    elif file_type == "pdf-to-excel":
        await pdf_to_excel(input_path, output_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

    return {"output_file": output_path}

def save_base64_file(file_content: str,file_name: str = "uploaded_file") -> str:
    """
    Saves Base64-encoded content to a file.
    """
    decoded_data = base64.b64decode(file_content)
    input_path = os.path.join(UPLOAD_DIR, file_name)
    with open(input_path, "wb") as f:
        f.write(decoded_data)
    return input_path

def generate_output_path(input_path: str, file_type: str) -> str:
    """
    Generates the output file path based on the input file and type.
    """
    extensions = {
        "jpg-to-pdf": ".pdf",
        "word-to-pdf": ".pdf",
        "excel-to-pdf": ".pdf",
        "ppt-to-pdf": ".pdf",
        "html-to-pdf": ".pdf",
        "pdf-to-jpg": "_page.jpg",
        "pdf-to-word": ".docx",
        "pdf-to-ppt": ".pptx",
        "pdf-to-excel": ".xlsx",
    }
    extension = extensions.get(file_type, "")
    return os.path.join(OUTPUT_DIR, Path(input_path).stem + extension)

async def jpg_to_pdf(input_path: str, output_path: str):
    with open(output_path, "wb") as pdf_file:
        pdf_file.write(img2pdf.convert(input_path))

async def word_to_pdf(input_path: str, output_path: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    doc = Document(input_path)
    for paragraph in doc.paragraphs:
        pdf.cell(200, 10, txt=paragraph.text, ln=True)
    pdf.output(output_path)

async def excel_to_pdf(input_path: str, output_path: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    df = pd.read_excel(input_path)
    for _, row in df.iterrows():
        pdf.cell(200, 10, txt=str(row.values), ln=True)
    pdf.output(output_path)

async def ppt_to_pdf(input_path: str, output_path: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    ppt = Presentation(input_path)
    for slide in ppt.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                pdf.cell(200, 10, txt=shape.text, ln=True)
    pdf.output(output_path)

async def html_to_pdf(input_path: str, output_path: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    with open(input_path, "r") as html_file:
        for line in html_file:
            pdf.cell(200, 10, txt=line.strip(), ln=True)
    pdf.output(output_path)

async def pdf_to_jpg(input_path: str):
    images = convert_from_path(input_path)
    output_files = []
    for i, image in enumerate(images):
        output_path = os.path.join(OUTPUT_DIR, f"{Path(input_path).stem}_{i + 1}.jpg")
        image.save(output_path, "JPEG")
        output_files.append(output_path)
    return {"output_files": output_files}

async def pdf_to_word(input_path: str, output_path: str):
    reader = PdfReader(input_path)
    doc = Document()
    for page in reader.pages:
        doc.add_paragraph(page.extract_text())
    doc.save(output_path)

async def pdf_to_ppt(input_path: str, output_path: str):
    reader = PdfReader(input_path)
    ppt = Presentation()
    for page in reader.pages:
        slide = ppt.slides.add_slide(ppt.slide_layouts[5])
        textbox = slide.shapes.add_textbox(left=0, top=0, width=720, height=540)
        textbox.text = page.extract_text()
    ppt.save(output_path)

async def pdf_to_excel(input_path: str, output_path: str):
    reader = PdfReader(input_path)
    data = []
    for page in reader.pages:
        data.append([line for line in page.extract_text().splitlines()])
    df = pd.DataFrame(data)
    df.to_excel(output_path, index=False, header=False)
