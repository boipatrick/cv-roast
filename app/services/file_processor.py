import os
import uuid
from typing import Tuple
from fastapi import UploadFile, HTTPException, status
from pypdf import PdfReader
import pdfplumber
from docx import Document
from ..config import get_settings

settings = get_settings()

class FileProcessor:
    def __init__(self):
        self.upload_dir = settings.UPLOAD_DIR
        self.max_size = settings.MAX_FILE_SIZE_MB * 1024 * 1024  # Convert to bytes
    
    async def save_uploaded_file(self, file: UploadFile) -> Tuple[str, str]:
        """Save uploaded file and return (filename, filepath)"""
        # Generate unique filename
        file_ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(self.upload_dir, unique_filename)
        
        # Check file size
        content = await file.read()
        if len(content) > self.max_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large. Max size: {settings.MAX_FILE_SIZE_MB}MB"
            )
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(content)
        
        return unique_filename, file_path
    
    def extract_text_from_file(self, file_path: str) -> str:
        """Extract text from uploaded file"""
        file_ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_ext == ".pdf":
                return self._extract_from_pdf(file_path)
            elif file_ext == ".docx":
                return self._extract_from_docx(file_path)
            elif file_ext == ".txt":
                return self._extract_from_txt(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_ext}")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Failed to extract text: {str(e)}"
            )
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF"""
        text = ""
        
        # Try with pdfplumber first (better for complex layouts)
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception :
            # Fallback to PyPDF2
            with open(file_path, 'rb') as file:
                pdf_reader = PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        
        return text.strip()
    
    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX"""
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    
    def _extract_from_txt(self, file_path: str) -> str:
        """Extract text from TXT"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
