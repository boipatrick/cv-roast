# app/api/v1/roast.py
from fastapi import APIRouter, Depends, HTTPException, status
from ...dependencies import get_roast_service
from ...schemas.roast import RoastRequest, RoastResponse
from ...services.roast_service import RoastService

router = APIRouter()

@router.post("/{cv_upload_id}", response_model=RoastResponse)
async def roast_cv(
    cv_upload_id: int,
    roast_request: RoastRequest,
    roast_service: RoastService = Depends(get_roast_service)
):
    """Generate a brutal roast of the uploaded CV"""
    try:
        roast_session = await roast_service.create_roast(cv_upload_id, roast_request)
        return roast_session
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate roast: {str(e)}"
        )

@router.get("/{roast_id}", response_model=RoastResponse)
async def get_roast(
    roast_id: int,
    roast_service: RoastService = Depends(get_roast_service)
):
    """Get a specific roast by ID"""
    roast = roast_service.get_roast_by_id(roast_id)
    if not roast:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Roast not found"
        )
    return roast

