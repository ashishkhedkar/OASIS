from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="OASIS API",
    description="Oceanic Attribution & Spill Intelligence System",
    version="1.0.0"
)

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to OASIS API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
