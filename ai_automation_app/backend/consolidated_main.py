"""
Consolidated FastAPI Main Application
- Simplified architecture with 4 core services
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Import consolidated services
from services.consolidated.user_management import router as user_router
from services.consolidated.patient_records import router as patient_router
from services.consolidated.clinical_operations import router as clinical_router
from services.financial.financial_api import router as financial_router

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Therastack API",
    description="Consolidated API for Therastack healthcare platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_router)
app.include_router(patient_router)
app.include_router(clinical_router)
app.include_router(financial_router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Therastack API",
        "documentation": "/docs",
        "status": "online"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
