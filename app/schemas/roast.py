from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from ..config import RoastLevel

class RoastRequest(BaseModel):
    roast_level: RoastLevel = RoastLevel.SAVAGE
    focus_areas: Optional[List[str]] = None  # ["experience", "skills", "formatting", "grammar"]

class RoastResponse(BaseModel):
    id: int
    roast_content: str
    roast_score: float
    roast_level: str
    categories_roasted: List[str]
    processing_time: float
    created_at: datetime
    
    class Config:
        from_attributes = True

class RoastSummary(BaseModel):
    total_roasts: int
    average_score: float
    most_roasted_category: str
    latest_roast: Optional[RoastResponse] = None

