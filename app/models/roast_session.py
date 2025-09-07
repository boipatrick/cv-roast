from sqlalchemy import Column, String, Text, Integer, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel

class RoastSession(BaseModel):
    __tablename__ = "roast_sessions"
    
    cv_upload_id = Column(Integer, ForeignKey("cv_uploads.id"), nullable=False)
    roast_level = Column(String, nullable=False)
    roast_content = Column(Text, nullable=False)
    roast_score = Column(Float)  # 0-10 brutality score
    categories_roasted = Column(JSON)  # ["formatting", "experience", "skills"]
    processing_time = Column(Float)  # seconds
    llm_model = Column(String)  # which model was used
    
    # Relationships
    cv_upload = relationship("CVUpload", back_populates="roast_sessions")

