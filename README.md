# File Conversion API

A FastAPI-based service for converting various file formats.

## Features
- Convert JPG to PDF
- Convert Word, Excel, PowerPoint, and HTML to PDF
- Convert PDF to JPG, Word, Excel, and PowerPoint

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `uvicorn app.main:app --reload`

## Using Docker
1. Build the image: `docker build -t file-conversion-api .`
2. Run the container: `docker-compose up`

## API Endpoints
- `POST /convert/jpg-to-pdf/`
- `POST /convert/pdf-to-word/`
