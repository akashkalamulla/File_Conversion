import base64
import tempfile
import os
import uuid
from io import BytesIO
from fpdf import FPDF
from PIL import Image
import img2pdf
from pdf2image import convert_from_path
from docx import Document
from pptx import Presentation
import pandas as pd
import pdfplumber
from PyPDF2 import PdfReader

# Define a folder to store converted files
SAVE_FOLDER = "converted_files"
os.makedirs(SAVE_FOLDER, exist_ok=True)  # Ensure folder exists

def encode_io_to_base64(file_io: BytesIO) -> str:
    """Encodes a BytesIO object to a Base64 string."""
    file_io.seek(0)
    return base64.b64encode(file_io.read()).decode("utf-8")


async def jpg_to_pdf(input_io: BytesIO) -> BytesIO:
    """Converts JPG or PNG to PDF."""
    try:
        output_io = BytesIO()
        output_io.write(img2pdf.convert(input_io))
        output_io.seek(0)
        return output_io
    except Exception as e:
        raise ValueError(f"JPG-to-PDF conversion failed: {e}")


async def word_to_pdf(input_io: BytesIO) -> BytesIO:
    """Converts Word document to PDF."""
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


async def excel_to_pdf(input_io: BytesIO) -> str:
    """Converts an Excel spreadsheet to a PDF file and saves it with a unique name."""
    try:
        input_io.seek(0)  # Move to the start of the file

        # Read Excel file directly from BytesIO
        df = pd.read_excel(input_io, engine="openpyxl")

        # Generate a unique filename
        file_id = str(uuid.uuid4())[:8]  # Create a short unique ID
        pdf_filename = os.path.join(SAVE_FOLDER, f"converted_{file_id}.pdf")

        # Create a PDF file
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=10)

        # Write table headers
        for col in df.columns:
            pdf.cell(40, 10, col, border=1)
        pdf.ln()

        # Write table rows
        for _, row in df.iterrows():
            for cell in row:
                pdf.cell(40, 10, str(cell), border=1)
            pdf.ln()

        pdf.output(pdf_filename)  # Save the file

        return pdf_filename  # Return saved file path

    except Exception as e:
        raise ValueError(f"Excel-to-PDF conversion failed: {e}")

async def ppt_to_pdf(input_io: BytesIO) -> BytesIO:
    """Converts PowerPoint presentations to PDF."""
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
    """Converts HTML content to PDF."""
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
    """Converts PDF pages to JPG images."""
    try:
        with tempfile.NamedTemporaryFile(delete=True, suffix=".pdf") as temp_pdf:
            temp_pdf.write(input_io.read())
            temp_pdf.flush()

            images = convert_from_path(temp_pdf.name)
            output_files = []
            for image in images:
                output_io = BytesIO()
                image.save(output_io, "JPEG")
                output_io.seek(0)
                output_files.append(encode_io_to_base64(output_io))

        return output_files
    except Exception as e:
        raise ValueError(f"PDF-to-JPG conversion failed: {e}")


async def pdf_to_word(input_io: BytesIO) -> BytesIO:
    """Converts PDF to editable Word document."""
    try:
        output_io = BytesIO()
        doc = Document()

        with pdfplumber.open(input_io) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    doc.add_paragraph(text)

        doc.save(output_io)
        output_io.seek(0)
        return output_io
    except Exception as e:
        raise ValueError(f"PDF-to-Word conversion failed: {e}")


async def pdf_to_ppt(input_io: BytesIO) -> BytesIO:
    """Converts PDF pages into PowerPoint slides."""
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
    """Extracts table data from PDF and converts it to an Excel spreadsheet."""
    try:
        output_io = BytesIO()
        data = []

        with pdfplumber.open(input_io) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        data.append(row)

        df = pd.DataFrame(data)
        df.to_excel(output_io, index=False, header=False)
        output_io.seek(0)
        return output_io
    except Exception as e:
        raise ValueError(f"PDF-to-Excel conversion failed: {e}")
