from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base

class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    confidence = Column(Float)
    area = Column(Float)
    polygon_wkt = Column(String)  # WKT representation of the segmented slick

class VesselRecord(Base):
    __tablename__ = "vessel_records"

    id = Column(Integer, primary_key=True, index=True)
    mmsi = Column(String, index=True)
    timestamp = Column(DateTime, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    speed = Column(Float)
    heading = Column(Float)
    status = Column(String)
