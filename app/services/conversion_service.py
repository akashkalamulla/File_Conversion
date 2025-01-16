import base64
from io import BytesIO
from fpdf import FPDF
from PIL import Image
import img2pdf
from pdf2image import convert_from_path
from docx import Document
from pptx import Presentation
import pandas as pd
from PyPDF2 import PdfReader

def encode_io_to_base64(file_io: BytesIO) -> str:
    """
    Encodes a BytesIO object to a Base64 string.
    """
    file_io.seek(0)
    return base64.b64encode(file_io.read()).decode("utf-8")

async def jpg_to_pdf(input_io: BytesIO) -> BytesIO:
    try:
        output_io = BytesIO()
        output_io.write(img2pdf.convert(input_io))
        output_io.seek(0)
        return output_io
    except Exception as e:
        raise ValueError(f"JPG-to-PDF conversion failed: {e}")

async def word_to_pdf(input_io: BytesIO) -> BytesIO:
    try:
        output_io = BytesIO()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        doc = Document(input_io)
        for paragraph in doc.paragraphs:
            pdf.multi_cell(0, 10, txt=paragraph.text)
        pdf.output(output_io)
        output_io.seek(0)
        return output_io
    except Exception as e:
        raise ValueError(f"Word-to-PDF conversion failed: {e}")

async def excel_to_pdf(input_io: BytesIO) -> BytesIO:
    try:
        output_io = BytesIO()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        df = pd.read_excel(input_io)
        for _, row in df.iterrows():
            pdf.multi_cell(0, 10, txt=str(row.values))
        pdf.output(output_io)
        output_io.seek(0)
        return output_io
    except Exception as e:
        raise ValueError(f"Excel-to-PDF conversion failed: {e}")

async def ppt_to_pdf(input_io: BytesIO) -> BytesIO:
    try:
        output_io = BytesIO()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        ppt = Presentation(input_io)
        for slide in ppt.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    pdf.multi_cell(0, 10, txt=shape.text)
        pdf.output(output_io)
        output_io.seek(0)
        return output_io
    except Exception as e:
        raise ValueError(f"PPT-to-PDF conversion failed: {e}")

async def html_to_pdf(input_io: BytesIO) -> BytesIO:
    try:
        output_io = BytesIO()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in input_io.read().decode("utf-8", errors="replace").splitlines():
            pdf.multi_cell(0, 10, txt=line.strip())
        pdf.output(output_io)
        output_io.seek(0)
        return output_io
    except Exception as e:
        raise ValueError(f"HTML-to-PDF conversion failed: {e}")

async def pdf_to_jpg(input_io: BytesIO):
    try:
        images = convert_from_path(input_io)
        output_files = []
        for i, image in enumerate(images):
            output_io = BytesIO()
            image.save(output_io, "JPEG")
            output_io.seek(0)
            output_files.append(encode_io_to_base64(output_io))
        return output_files
    except Exception as e:
        raise ValueError(f"PDF-to-JPG conversion failed: {e}")

async def pdf_to_word(input_io: BytesIO) -> BytesIO:
    try:
        output_io = BytesIO()
        reader = PdfReader(input_io)
        doc = Document()
        for page in reader.pages:
            text = page.extract_text()
            if text:
                doc.add_paragraph(text)
        doc.save(output_io)
        output_io.seek(0)
        return output_io
    except Exception as e:
        raise ValueError(f"PDF-to-Word conversion failed: {e}")

async def pdf_to_ppt(input_io: BytesIO) -> BytesIO:
    try:
        output_io = BytesIO()
        reader = PdfReader(input_io)
        ppt = Presentation()
        for page in reader.pages:
            text = page.extract_text()
            if text:
                slide = ppt.slides.add_slide(ppt.slide_layouts[5])
                textbox = slide.shapes.add_textbox(left=0, top=0, width=720, height=540)
                textbox.text = text
        ppt.save(output_io)
        output_io.seek(0)
        return output_io
    except Exception as e:
        raise ValueError(f"PDF-to-PPT conversion failed: {e}")

async def pdf_to_excel(input_io: BytesIO) -> BytesIO:
    try:
        output_io = BytesIO()
        reader = PdfReader(input_io)
        data = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                data.append([line for line in text.splitlines()])
        df = pd.DataFrame(data)
        df.to_excel(output_io, index=False, header=False)
        output_io.seek(0)
        return output_io
    except Exception as e:
        raise ValueError(f"PDF-to-Excel conversion failed: {e}")
