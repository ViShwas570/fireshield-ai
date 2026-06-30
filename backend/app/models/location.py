"""
FireShield AI - Location Models

Pydantic models for nearby emergency services (fire stations, hospitals, police stations).
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class NearbyRequest(BaseModel):
    """Schema for requesting nearby services."""
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lng: float = Field(..., ge=-180, le=180, description="Longitude")
    radius_km: float = Field(default=10.0, ge=0.1, le=50.0, description="Search radius in km")


class NearbyStation(BaseModel):
    """Schema for a nearby fire station."""
    id: str = Field(..., description="Station identifier")
    name: str = Field(..., description="Fire station name")
    lat: float = Field(..., description="Latitude")
    lng: float = Field(..., description="Longitude")
    address: str = Field(..., description="Full address")
    phone: str = Field(..., description="Contact phone number")
    distance_km: float = Field(..., description="Distance from query point in km")
    available_units: int = Field(..., ge=0, description="Number of available fire units")


class NearbyHospital(BaseModel):
    """Schema for a nearby hospital."""
    id: str = Field(..., description="Hospital identifier")
    name: str = Field(..., description="Hospital name")
    lat: float = Field(..., description="Latitude")
    lng: float = Field(..., description="Longitude")
    address: str = Field(..., description="Full address")
    phone: str = Field(..., description="Contact phone number")
    distance_km: float = Field(..., description="Distance from query point in km")
    emergency_available: bool = Field(default=True, description="Whether emergency services are available")
    burn_unit: bool = Field(default=False, description="Whether a burn unit is available")


class NearbyPolice(BaseModel):
    """Schema for a nearby police station."""
    id: str = Field(..., description="Station identifier")
    name: str = Field(..., description="Police station name")
    lat: float = Field(..., description="Latitude")
    lng: float = Field(..., description="Longitude")
    address: str = Field(..., description="Full address")
    phone: str = Field(..., description="Contact phone number")
    distance_km: float = Field(..., description="Distance from query point in km")


class NearbyServicesResponse(BaseModel):
    """Combined response for all nearby services."""
    fire_stations: List[NearbyStation] = Field(default_factory=list)
    hospitals: List[NearbyHospital] = Field(default_factory=list)
    police_stations: List[NearbyPolice] = Field(default_factory=list)
