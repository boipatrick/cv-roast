from sqlalchemy.orm import Session
from typing import List, Optional
import time
from ..models.cv_upload import CVUpload
from ..models.roast_session import RoastSession
from ..schemas.roast import RoastRequest
from .file_processor import FileProcessor
from .llm_service import LLMService

class RoastService:
    def __init__(self, db: Session):
        self.db = db
        self.file_processor = FileProcessor()
        self.llm_service = LLMService()
    
    async def create_roast(self, cv_upload_id: int, roast_request: RoastRequest) -> RoastSession:
        """Create a new roast session"""
        # Get CV upload
        cv_upload = self.db.query(CVUpload).filter(CVUpload.id == cv_upload_id).first()
        if not cv_upload:
            raise ValueError("CV upload not found")
        
        if not cv_upload.extracted_text:
            raise ValueError("CV text not extracted yet")
        
        # Generate roast
        start_time = time.time()
        roast_result = await self.llm_service.generate_roast(
            cv_upload.extracted_text,
            roast_request.roast_level.value,
            roast_request.focus_areas
        )
        processing_time = time.time() - start_time
        
        # Create roast session
        roast_session = RoastSession(
            cv_upload_id=cv_upload_id,
            roast_level=roast_request.roast_level.value,
            roast_content=roast_result["roast"],
            roast_score=roast_result["score"],
            categories_roasted=roast_result["categories"],
            processing_time=processing_time,
            llm_model=roast_result["model"]
        )
        
        self.db.add(roast_session)
        self.db.commit()
        self.db.refresh(roast_session)
        
        return roast_session
    
    def get_roast_history(self, limit: int = 10) -> List[RoastSession]:
        """Get recent roast history"""
        return self.db.query(RoastSession).order_by(RoastSession.created_at.desc()).limit(limit).all()
    
    def get_roast_by_id(self, roast_id: int) -> Optional[RoastSession]:
        """Get roast by ID"""
        return self.db.query(RoastSession).filter(RoastSession.id == roast_id).first()
