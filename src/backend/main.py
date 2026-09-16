"""
OASIS - Backend API

M5: Backend / Integration
Provides API endpoints for connecting the segmentation,
drift, and AIS modules.
"""

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from src.segmentation.inference import detect_oil
from src.drift.inference import predict_origins
from src.ais.inference import predict_vessels


app = FastAPI(
    title="OASIS",
    description="Oil Spill Detection and Vessel Attribution API",
    version="1.0.0",
)


class AnalysisRequest(BaseModel):
    """Input data required to start an OASIS analysis."""

    latitude: float
    longitude: float
    timestamp: str


@app.get("/")
def root():
    """Basic health check for the backend."""
    return {
        "project": "OASIS",
        "status": "Backend is running",
    }


@app.get("/health")
def health_check():
    """Return backend health status."""
    return {
        "status": "healthy",
    }


@app.post("/detect")
async def detect_oil_spill(file: UploadFile = File(...)):
    """Run the M2 U-Net model on an uploaded SAR image."""

    # Save the uploaded image temporarily so M2 can process it.
    temp_path = f"/tmp/{file.filename}"

    with open(temp_path, "wb") as buffer:
        buffer.write(await file.read())

    # Run the trained segmentation model.
    oil_mask = detect_oil(temp_path)

    # Count pixels classified as oil.
    oil_pixels = int(oil_mask.sum())

    return {
        "filename": file.filename,
        "oil_detected": oil_pixels > 0,
        "oil_pixels": oil_pixels,
    }


@app.post("/drift")
def drift_analysis(request: AnalysisRequest):
    """Generate possible spill-origin points using the M3 drift module."""

    origins = predict_origins(
        latitude=request.latitude,
        longitude=request.longitude,
        timestamp=request.timestamp,
    )

    return {
        "candidate_origins": origins,
    }


@app.post("/vessels")
def vessel_analysis(request: AnalysisRequest):
    """Find and rank vessels near a suspected spill origin using M4."""

    results = predict_vessels(
        origin_latitude=request.latitude,
        origin_longitude=request.longitude,
        origin_time=request.timestamp,
    )

    # Convert the pandas result into JSON-compatible records for FastAPI.
    if results.empty:
        vessels = []
    else:
        vessels = results.to_dict(orient="records")

    return {
        "candidate_vessels": vessels,
    }