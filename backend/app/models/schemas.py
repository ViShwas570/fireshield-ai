"""Pydantic models for users, incidents, locations, chat, and analytics."""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import uuid

# ─── Enums ────────────────────────────────────────────────
class UserRole(str, Enum):
    citizen = "citizen"
    official = "official"
    admin = "admin"

class IncidentStatus(str, Enum):
    reported = "reported"
    acknowledged = "acknowledged"
    assigned = "assigned"
    en_route = "en_route"
    arrived = "arrived"
    resolved = "resolved"

class IncidentCategory(str, Enum):
    building = "building"
    industrial = "industrial"
    forest = "forest"
    vehicle = "vehicle"
    kitchen = "kitchen"
    electrical = "electrical"
    gas_leak = "gas_leak"
    other = "other"

# ─── User Models ──────────────────────────────────────────
class UserCreate(BaseModel):
    name: str
    email: str
    phone: str = ""
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    role: UserRole
    avatar_url: Optional[str] = None
    created_at: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# ─── Incident Models ─────────────────────────────────────
class IncidentCreate(BaseModel):
    title: str
    description: str = ""
    latitude: float
    longitude: float
    address: str = ""
    category: str = "other"
    media_urls: List[str] = []

class AIAnalysis(BaseModel):
    severity_score: float
    fire_type: str
    risk_level: str
    estimated_affected_area: str
    recommended_units: int
    analysis_text: str
    confidence_score: float

class StatusHistoryEntry(BaseModel):
    status: str
    timestamp: str
    updated_by: str = "system"
    notes: str = ""

class IncidentResponse(BaseModel):
    id: str
    user_id: str
    user_name: str = ""
    title: str
    description: str
    latitude: float
    longitude: float
    address: str
    category: str
    severity: int
    status: str
    media_urls: List[str]
    ai_analysis: Optional[AIAnalysis] = None
    assigned_team: Optional[str] = None
    created_at: str
    updated_at: str
    response_time_mins: Optional[float] = None
    status_history: List[StatusHistoryEntry] = []

class IncidentStatusUpdate(BaseModel):
    status: str
    assigned_team: Optional[str] = None
    notes: str = ""

class IncidentListResponse(BaseModel):
    incidents: List[IncidentResponse]
    total: int

# ─── SOS Model ────────────────────────────────────────────
class SOSRequest(BaseModel):
    latitude: float
    longitude: float
    description: str = "Emergency SOS"
    media_urls: List[str] = []

# ─── Location Models ─────────────────────────────────────
class NearbyService(BaseModel):
    id: str
    name: str
    latitude: float
    longitude: float
    address: str
    phone: str
    distance_km: float
    service_type: str
    available_units: Optional[int] = None
    has_burn_unit: Optional[bool] = None

# ─── Chat Models ─────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str
    lang: str = "en"

class ChatResponse(BaseModel):
    response: str
    suggestions: List[str]
    emergency_type: str = "general"

# ─── Analytics Models ────────────────────────────────────
class DashboardSummary(BaseModel):
    total_incidents: int
    active_incidents: int
    resolved_today: int
    avg_response_time_mins: float
    incidents_by_severity: Dict[str, int]
    incidents_by_status: Dict[str, int]
    monthly_trend: List[Dict[str, Any]]

class HeatmapPoint(BaseModel):
    latitude: float
    longitude: float
    intensity: float

class TimelineEvent(BaseModel):
    id: str
    type: str
    title: str
    description: str
    severity: int
    timestamp: str
