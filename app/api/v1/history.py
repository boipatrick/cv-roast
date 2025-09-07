from fastapi import APIRouter, Depends, Query
from typing import List
from ...dependencies import get_roast_service
from ...schemas.roast import RoastResponse
from ...services.roast_service import RoastService

router = APIRouter()

@router.get("/", response_model=List[RoastResponse])
async def get_roast_history(
    limit: int = Query(10, ge=1, le=100),
    roast_service: RoastService = Depends(get_roast_service)
):
    """Get recent roast history"""
    return roast_service.get_roast_history(limit)
