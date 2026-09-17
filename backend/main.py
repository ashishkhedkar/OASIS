import sys
import os
# Add the parent directory to sys.path so we can import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.database import engine, Base, get_db
import models
from src.data.sar_geolocation import extract_geolocation_points, RAW_SAR_DIR
from src.segmentation.inference import detect_oil, detect_oil_tiled
from src.drift.inference import predict_origins, group_origin_clusters, calculate_cluster_centers
from src.ais.inference import predict_vessels_from_origins
from typing import List
# Create database tables (if they don't exist yet)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SIH 2026 API",
    description="Backend API for SAR and AIS Data Processing",
    version="1.0.0"
)

# Configure CORS so the React frontend can talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "API is running perfectly"}

# --- Data Validation Schemas ---
class ShipCreate(BaseModel):
    mmsi: str
    name: str
    latitude: float
    longitude: float

class OilSpillCreate(BaseModel):
    image_name: str
    latitude: float
    longitude: float
    area_sq_km: float = None
    confidence: float = None

class DriftSimulationRequest(BaseModel):
    latitude: float
    longitude: float
    timestamp: str
    total_hours: int = 6

class CandidateOrigin(BaseModel):
    latitude: float
    longitude: float
    hours_back: float
    confidence: float = 0.8
    uncertainty_km: float = 5.0

class RankVesselsRequest(BaseModel):
    origins: List[CandidateOrigin]
    incident_timestamp: str

# --- New Endpoints ---

# 1. Add a new ship to the database
@app.post("/api/ships")
def create_ship(ship: ShipCreate, db: Session = Depends(get_db)):
    # Check if a ship with this MMSI already exists
    existing_ship = db.query(models.Ship).filter(models.Ship.mmsi == ship.mmsi).first()
    if existing_ship:
        raise HTTPException(status_code=400, detail="Ship with this MMSI already exists")

    # Create the new ship in the database
    db_ship = models.Ship(
        mmsi=ship.mmsi,
        name=ship.name,
        latitude=ship.latitude,
        longitude=ship.longitude
    )
    db.add(db_ship)
    db.commit()
    db.refresh(db_ship)
    return {"message": "Ship created successfully!", "ship": db_ship}

# 2. Get a list of all ships from the database
@app.get("/api/ships")
def get_ships(db: Session = Depends(get_db)):
    ships = db.query(models.Ship).all()
    return {"ships": ships}

# 3. Extract SAR Geolocation Metadata
@app.get("/api/process-sar")
def process_sar_data():
    xml_files = list(RAW_SAR_DIR.glob("*vv*.xml"))

    if not xml_files:
        raise HTTPException(status_code=404, detail="No VV annotation XML file found in data/raw/sar")

    try:
        points = extract_geolocation_points(xml_files[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process SAR XML: {str(e)}")

    return {
        "message": f"Successfully processed {len(points)} geolocation points!",
        "file_used": str(xml_files[0].name),
        "first_point": points[0] if points else None,
        "sample_points": points[:10]
    }

# 4. Trigger Oil Spill Detection
@app.post("/api/detect-spill")
def detect_spill(spill: OilSpillCreate, db: Session = Depends(get_db)):
    # Mocking ML detection for local demo since raw SAR files are not present locally
    try:
        confidence = 0.985
        area_sq_km = 12.50
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ML Inference failed: {str(e)}")

    # Save the result to the database
    db_spill = models.OilSpill(
        image_name=spill.image_name,
        latitude=spill.latitude,
        longitude=spill.longitude,
        area_sq_km=area_sq_km,
        confidence=confidence
    )
    db.add(db_spill)
    db.commit()
    db.refresh(db_spill)
    return {"message": "Spill detected and saved to database!", "spill": db_spill}

# 5. Get History of detected spills
@app.get("/api/spills")
def get_spills(db: Session = Depends(get_db)):
    spills = db.query(models.OilSpill).all()
    return {"spills": spills}

# 6. Simulate Ocean Drift
@app.post("/api/simulate-drift")
def simulate_drift(req: DriftSimulationRequest):
    # Mocking for local demo
    try:
        centers = [
            {"latitude": req.latitude - 0.05, "longitude": req.longitude - 0.05, "hours_back": 1, "confidence": 0.95, "uncertainty_km": 1.2},
            {"latitude": req.latitude - 0.10, "longitude": req.longitude - 0.10, "hours_back": 2, "confidence": 0.88, "uncertainty_km": 2.5},
            {"latitude": req.latitude - 0.15, "longitude": req.longitude - 0.15, "hours_back": 3, "confidence": 0.82, "uncertainty_km": 3.8},
            {"latitude": req.latitude - 0.20, "longitude": req.longitude - 0.20, "hours_back": 4, "confidence": 0.75, "uncertainty_km": 5.0},
            {"latitude": req.latitude - 0.25, "longitude": req.longitude - 0.25, "hours_back": 5, "confidence": 0.60, "uncertainty_km": 7.5}
        ]
        return {"centers": centers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Drift simulation failed: {str(e)}")

# 7. Rank Candidate Vessels
@app.post("/api/rank-vessels")
def rank_vessels(req: RankVesselsRequest):
    # Mocking for local demo
    try:
        results = [
            {"MMSI": "419001234", "LAT": 13.1, "LON": 80.2, "attribution_score": 0.94, "temporal_score": 0.3, "spatial_score": 0.9},
            {"MMSI": "419005678", "LAT": 13.0, "LON": 80.1, "attribution_score": 0.87, "temporal_score": 0.9, "spatial_score": 0.9},
            {"MMSI": "419009876", "LAT": 12.9, "LON": 80.0, "attribution_score": 0.79, "temporal_score": 0.6, "spatial_score": 0.8},
            {"MMSI": "419004321", "LAT": 12.8, "LON": 79.9, "attribution_score": 0.71, "temporal_score": 0.7, "spatial_score": 0.4}
        ]
        return {"ranked_vessels": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vessel ranking failed: {str(e)}")

# Serve the HTML frontend files from the "frontend_ui" folder at the root URL
frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend_ui')
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="site")

if __name__ == "__main__":
    import uvicorn
    # To run the server, use this command in your terminal:
    # cd backend
    # uvicorn main:app --reload
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
