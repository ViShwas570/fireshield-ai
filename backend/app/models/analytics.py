"""
FireShield AI - Analytics Models

Pydantic models for dashboard analytics, heatmaps, and trend data.
"""

from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import datetime


class DashboardSummary(BaseModel):
    """Summary statistics for the analytics dashboard."""
    total_incidents: int = Field(..., description="Total incidents ever reported")
    active_incidents: int = Field(..., description="Currently active (unresolved) incidents")
    resolved_today: int = Field(..., description="Incidents resolved today")
    avg_response_time: float = Field(..., description="Average response time in minutes")
    incidents_by_severity: Dict[str, int] = Field(
        default_factory=dict, description="Count of incidents grouped by severity (1-5)"
    )
    incidents_by_status: Dict[str, int] = Field(
        default_factory=dict, description="Count of incidents grouped by status"
    )


class HeatmapPoint(BaseModel):
    """A single point on the incident heatmap."""
    lat: float = Field(..., description="Latitude")
    lng: float = Field(..., description="Longitude")
    intensity: float = Field(..., ge=0, le=1, description="Heat intensity (0-1)")
    incident_id: str = Field(..., description="Related incident ID")
    severity: int = Field(..., description="Incident severity")


class TimelineEntry(BaseModel):
    """A single entry in the event timeline."""
    id: str = Field(..., description="Event identifier")
    incident_id: str = Field(..., description="Related incident ID")
    title: str = Field(..., description="Event title")
    description: str = Field(..., description="Event description")
    status: str = Field(..., description="Status at this point")
    timestamp: datetime = Field(..., description="Event timestamp")
    severity: int = Field(..., description="Incident severity")
    address: str = Field(..., description="Incident address")


class MonthlyTrend(BaseModel):
    """Monthly incident trend data."""
    month: str = Field(..., description="Month label (e.g., 'Jan 2026')")
    total: int = Field(..., description="Total incidents in the month")
    resolved: int = Field(..., description="Resolved incidents in the month")
    avg_response_time: float = Field(..., description="Avg response time in minutes")


class AnalyticsResponse(BaseModel):
    """Complete analytics response combining all analytics data."""
    summary: DashboardSummary = Field(..., description="Dashboard summary stats")
    monthly_trend: List[MonthlyTrend] = Field(default_factory=list, description="Monthly trend data")
    heatmap: List[HeatmapPoint] = Field(default_factory=list, description="Heatmap data points")
    recent_timeline: List[TimelineEntry] = Field(default_factory=list, description="Recent event timeline")
