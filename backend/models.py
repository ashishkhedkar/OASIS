from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
import datetime

# Example Model: This tells the database how to create the 'ships' table
class Ship(Base):
    __tablename__ = "ships"

    id = Column(Integer, primary_key=True, index=True)
    mmsi = Column(String, unique=True, index=True) # Maritime Mobile Service Identity
    name = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)

# Model for saving detected oil spills
class OilSpill(Base):
    __tablename__ = "oil_spills"

    id = Column(Integer, primary_key=True, index=True)
    image_name = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    area_sq_km = Column(Float, nullable=True)
    confidence = Column(Float, nullable=True)
    detected_at = Column(DateTime, default=datetime.datetime.utcnow)
