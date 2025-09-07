from sqlalchemy import Column, String, Text, Integer
from sqlalchemy.orm import relationship
from .base import BaseModel

class CVUpload(BaseModel):
    __tablename__ = "cv_uploads"
    
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    content_type = Column(String, nullable=False)
    extracted_text = Column(Text)
    processing_status = Column(String, default="pending")  # pending, processed, failed
    
    # Relationships
    roast_sessions = relationship("RoastSession", back_populates="cv_upload")
