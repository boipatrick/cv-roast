from fastapi import Depends, HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from .database import get_db
from .config import get_settings
from .services.file_processor import FileProcessor
from .services.roast_service import RoastService
import os

settings = get_settings()

def validate_file_upload(file: UploadFile):
    """Validate uploaded file"""
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file uploaded"
        )
    
    # Check file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file_ext} not allowed. Supported: {settings.ALLOWED_EXTENSIONS}"
        )
    
    return file

def get_file_processor():
    """Get file processor service"""
    return FileProcessor()

def get_roast_service(db: Session = Depends(get_db)):
    """Get roasting service"""
    return RoastService(db)