from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CVUploadResponse(BaseModel):
    id: int
    filename: str
    original_filename: str
    file_size: int
    processing_status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class CVProcessingStatus(BaseModel):
    upload_id: int
    status: str
    extracted_text: Optional[str] = None
    error_message: Optional[str] = None