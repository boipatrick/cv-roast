
# app/api/v1/router.py
from fastapi import APIRouter
from .upload import router as upload_router
from .roast import router as roast_router
from .history import router as history_router

api_router = APIRouter()

api_router.include_router(upload_router, prefix="/upload", tags=["File Upload"])
api_router.include_router(roast_router, prefix="/roast", tags=["CV Roasting"])
api_router.include_router(history_router, prefix="/history", tags=["Roast History"])

