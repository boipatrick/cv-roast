from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import get_settings
from .api.v1.router import api_router
import os

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description="Upload your CV and get absolutely roasted by AI 🔥",
    version=settings.API_VERSION,
    debug=settings.DEBUG,
)

# Create upload directory
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files (for serving uploaded files if needed)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include routers
app.include_router(api_router, prefix=f"/api/{settings.API_VERSION}")

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "description": "Upload your CV and prepare to get roasted! 🔥",
        "endpoints": {
            "upload": "/api/v1/upload",
            "roast": "/api/v1/roast",
            "history": "/api/v1/history"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "ready_to_roast", "fire": "🔥🔥🔥"}