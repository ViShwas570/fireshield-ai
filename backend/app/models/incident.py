"""
FireShield AI - Incident Models

Pydantic models for fire incident reporting, tracking, AI analysis, and SOS requests.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class IncidentStatus(str, Enum):
    """Status progression of a fire incident."""
    REPORTED = "reported"
    ACKNOWLEDGED = "acknowledged"
    ASSIGNED = "assigned"
    EN_ROUTE = "en_route"
    ARRIVED = "arrived"
    RESOLVED = "resolved"


class FireType(str, Enum):
    """Classification of fire types."""
    BUILDING = "building_fire"
    INDUSTRIAL = "industrial_fire"
    FOREST = "forest_fire"
    ELECTRICAL = "electrical_fire"
    KITCHEN = "kitchen_fire"
    VEHICLE = "vehicle_fire"
    GAS_LEAK = "gas_leak_fire"
    CHEMICAL = "chemical_fire"
    UNKNOWN = "unknown"


class RiskLevel(str, Enum):
    """Risk assessment levels."""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"
    EXTREME = "extreme"


class AIAnalysis(BaseModel):
    """AI-generated analysis of a fire incident."""
    severity_score: float = Field(..., ge=0, le=10, description="AI severity score (0-10)")
    fire_type: FireType = Field(..., description="Classified fire type")
    risk_level: RiskLevel = Field(..., description="Overall risk assessment")
    estimated_affected_area: str = Field(..., description="Estimated affected area in sq meters")
    recommended_units: int = Field(..., ge=1, description="Recommended fire units to dispatch")
    analysis_text: str = Field(..., description="Detailed AI analysis narrative")
    confidence_score: float = Field(..., ge=0, le=1, description="AI confidence (0-1)")
    recommended_actions: List[str] = Field(default_factory=list, description="Recommended response actions")


class IncidentCreate(BaseModel):
    """Schema for creating a new fire incident report."""
    title: str = Field(..., min_length=5, max_length=200, description="Brief incident title")
    description: str = Field(..., min_length=10, description="Detailed incident description")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate")
    address: str = Field(..., min_length=5, description="Full address of the incident")
    severity: int = Field(..., ge=1, le=5, description="Reported severity (1-5)")
    media_urls: List[str] = Field(default_factory=list, description="URLs of uploaded media")


class IncidentResponse(BaseModel):
    """Schema for incident data in API responses."""
    id: str = Field(..., description="Unique incident identifier")
    user_id: str = Field(..., description="Reporter's user ID")
    title: str = Field(..., description="Incident title")
    description: str = Field(..., description="Incident description")
    latitude: float = Field(..., description="Latitude")
    longitude: float = Field(..., description="Longitude")
    address: str = Field(..., description="Full address")
    severity: int = Field(..., description="Severity level (1-5)")
    status: IncidentStatus = Field(..., description="Current status")
    media_urls: List[str] = Field(default_factory=list, description="Media file URLs")
    ai_analysis: Optional[AIAnalysis] = Field(None, description="AI analysis results")
    assigned_team: Optional[str] = Field(None, description="Assigned fire team/station")
    created_at: datetime = Field(..., description="Report creation time")
    updated_at: datetime = Field(..., description="Last update time")
    response_time_mins: Optional[float] = Field(None, description="Response time in minutes")
    reporter_name: Optional[str] = Field(None, description="Name of the person who reported")


class IncidentUpdate(BaseModel):
    """Schema for updating an incident."""
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    description: Optional[str] = Field(None, min_length=10)
    severity: Optional[int] = Field(None, ge=1, le=5)
    address: Optional[str] = None
    assigned_team: Optional[str] = None


class IncidentStatusUpdate(BaseModel):
    """Schema for updating incident status."""
    status: IncidentStatus = Field(..., description="New status")
    notes: Optional[str] = Field(None, description="Status update notes")


class SOSRequest(BaseModel):
    """Schema for emergency SOS request."""
    latitude: float = Field(..., ge=-90, le=90, description="Current latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Current longitude")
    description: Optional[str] = Field("Emergency SOS - Fire reported", description="Brief description")
    phone: Optional[str] = Field(None, description="Contact phone number")
