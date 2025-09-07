from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from ...database import get_db
from ...dependencies import validate_file_upload, get_file_processor
from ...models.cv_upload import CVUpload
from ...schemas.cv import CVUploadResponse, CVProcessingStatus
from ...services.file_processor import FileProcessor
import os

router = APIRouter()

async def process_cv_text(cv_upload_id: int, file_path: str, db: Session):
    """Background task to process CV text"""
    file_processor = FileProcessor()
    cv_upload = db.query(CVUpload).filter(CVUpload.id == cv_upload_id).first()
    
    try:
        extracted_text = file_processor.extract_text_from_file(file_path)
        cv_upload.extracted_text = extracted_text
        cv_upload.processing_status = "processed"
    except Exception :
        cv_upload.processing_status = "failed"
    
    db.commit()

@router.post("/", response_model=CVUploadResponse)
async def upload_cv(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="CV file (PDF, DOCX, or TXT)"),
    db: Session = Depends(get_db),
    file_processor: FileProcessor = Depends(get_file_processor)
):
    """Upload CV file for roasting"""
    # Validate file
    validate_file_upload(file)
    
    try:
        # Save file
        filename, file_path = await file_processor.save_uploaded_file(file)
        
        # Create database record
        cv_upload = CVUpload(
            filename=filename,
            original_filename=file.filename,
            file_path=file_path,
            file_size=file.size or os.path.getsize(file_path),
            content_type=file.content_type or "application/octet-stream",
            processing_status="pending"
        )
        
        db.add(cv_upload)
        db.commit()
        db.refresh(cv_upload)
        
        # Process text extraction in background
        background_tasks.add_task(process_cv_text, cv_upload.id, file_path, db)
        
        return cv_upload
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file: {str(e)}"
        )

@router.get("/{upload_id}/status", response_model=CVProcessingStatus)
async def get_processing_status(upload_id: int, db: Session = Depends(get_db)):
    """Get processing status of uploaded CV"""
    cv_upload = db.query(CVUpload).filter(CVUpload.id == upload_id).first()
    
    if not cv_upload:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CV upload not found"
        )
    
    return CVProcessingStatus(
        upload_id=cv_upload.id,
        status=cv_upload.processing_status,
        extracted_text=cv_upload.extracted_text if cv_upload.processing_status == "processed" else None
    )

