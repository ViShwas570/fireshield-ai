"""
FireShield AI - Incident Service

In-memory incident store with CRUD operations. Pre-seeded with 18 realistic
sample incidents across major Indian cities spanning the last 30 days.
"""

from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional
import random

from app.models.incident import (
    IncidentCreate,
    IncidentResponse,
    IncidentStatus,
    IncidentStatusUpdate,
    AIAnalysis,
    FireType,
    RiskLevel,
)
from app.utils.helpers import generate_uuid, now_utc


# In-memory incident store: id -> dict
_incidents_db: Dict[str, dict] = {}


def get_all_incidents(
    status_filter: Optional[str] = None,
    severity_filter: Optional[int] = None,
    search: Optional[str] = None,
) -> List[IncidentResponse]:
    """
    Retrieve all incidents with optional filters.

    Args:
        status_filter: Filter by incident status.
        severity_filter: Filter by severity level.
        search: Search in title, description, and address.

    Returns:
        List of matching IncidentResponse objects sorted by created_at desc.
    """
    results = []
    for inc_data in _incidents_db.values():
        if status_filter and inc_data["status"] != status_filter:
            continue
        if severity_filter and inc_data["severity"] != severity_filter:
            continue
        if search:
            search_lower = search.lower()
            searchable = f"{inc_data['title']} {inc_data['description']} {inc_data['address']}".lower()
            if search_lower not in searchable:
                continue
        results.append(IncidentResponse(**inc_data))

    results.sort(key=lambda x: x.created_at, reverse=True)
    return results


def get_incident_by_id(incident_id: str) -> Optional[IncidentResponse]:
    """
    Retrieve a single incident by ID.

    Args:
        incident_id: The incident UUID.

    Returns:
        IncidentResponse if found, None otherwise.
    """
    inc_data = _incidents_db.get(incident_id)
    if inc_data:
        return IncidentResponse(**inc_data)
    return None


def create_incident(
    incident_data: IncidentCreate,
    user_id: str,
    reporter_name: Optional[str] = None,
) -> IncidentResponse:
    """
    Create a new fire incident report.

    Args:
        incident_data: The incident creation data.
        user_id: ID of the reporting user.
        reporter_name: Name of the reporter.

    Returns:
        The created IncidentResponse.
    """
    incident_id = generate_uuid()
    now = now_utc()

    inc_dict = {
        "id": incident_id,
        "user_id": user_id,
        "title": incident_data.title,
        "description": incident_data.description,
        "latitude": incident_data.latitude,
        "longitude": incident_data.longitude,
        "address": incident_data.address,
        "severity": incident_data.severity,
        "status": IncidentStatus.REPORTED.value,
        "media_urls": incident_data.media_urls,
        "ai_analysis": None,
        "assigned_team": None,
        "created_at": now,
        "updated_at": now,
        "response_time_mins": None,
        "reporter_name": reporter_name,
    }

    _incidents_db[incident_id] = inc_dict
    return IncidentResponse(**inc_dict)


def update_incident_status(
    incident_id: str, status_update: IncidentStatusUpdate
) -> Optional[IncidentResponse]:
    """
    Update the status of an incident.

    Args:
        incident_id: The incident UUID.
        status_update: New status and optional notes.

    Returns:
        Updated IncidentResponse, or None if not found.
    """
    inc_data = _incidents_db.get(incident_id)
    if not inc_data:
        return None

    inc_data["status"] = status_update.status.value
    inc_data["updated_at"] = now_utc()

    # Calculate response time when status changes to "arrived"
    if status_update.status == IncidentStatus.ARRIVED and inc_data["response_time_mins"] is None:
        created = inc_data["created_at"]
        if isinstance(created, str):
            created = datetime.fromisoformat(created)
        delta = now_utc() - created
        inc_data["response_time_mins"] = round(delta.total_seconds() / 60, 1)

    _incidents_db[incident_id] = inc_data
    return IncidentResponse(**inc_data)


def set_incident_ai_analysis(
    incident_id: str, analysis: AIAnalysis
) -> Optional[IncidentResponse]:
    """
    Attach AI analysis results to an incident.

    Args:
        incident_id: The incident UUID.
        analysis: The AIAnalysis data.

    Returns:
        Updated IncidentResponse, or None if not found.
    """
    inc_data = _incidents_db.get(incident_id)
    if not inc_data:
        return None

    inc_data["ai_analysis"] = analysis.model_dump()
    inc_data["updated_at"] = now_utc()
    _incidents_db[incident_id] = inc_data
    return IncidentResponse(**inc_data)


def get_incidents_store() -> Dict[str, dict]:
    """Return a reference to the raw incidents store (for analytics)."""
    return _incidents_db


def seed_sample_incidents(citizen_user_id: str) -> None:
    """
    Pre-seed the incident store with 18 realistic sample incidents
    across major Indian cities, spread over the last 30 days.

    Args:
        citizen_user_id: The user ID to assign as the reporter.
    """
    now = now_utc()

    sample_incidents = [
        {
            "title": "Major Building Fire in Connaught Place",
            "description": "Large-scale fire broke out on the 3rd floor of a commercial building in Connaught Place. Thick black smoke visible from several blocks away. Multiple floors affected with risk of structural collapse. Approximately 50 people were inside at the time of fire.",
            "latitude": 28.6315,
            "longitude": 77.2167,
            "address": "Block A, Connaught Place, New Delhi, Delhi 110001",
            "severity": 5,
            "status": IncidentStatus.ARRIVED.value,
            "assigned_team": "Delhi Fire Station No. 1 - Connaught Place",
            "response_time_mins": 8.5,
            "days_ago": 1,
            "fire_type": FireType.BUILDING,
            "risk_level": RiskLevel.CRITICAL,
        },
        {
            "title": "Industrial Fire at Andheri Factory",
            "description": "Fire reported at a chemical processing factory in Andheri MIDC area. Hazardous materials involved including solvents and industrial chemicals. Strong chemical fumes spreading to nearby residential areas. Factory workers evacuated but two workers reported missing.",
            "latitude": 19.1197,
            "longitude": 72.8464,
            "address": "Plot 45, MIDC Industrial Area, Andheri East, Mumbai, Maharashtra 400093",
            "severity": 5,
            "status": IncidentStatus.EN_ROUTE.value,
            "assigned_team": "Mumbai Fire Brigade - Andheri Station",
            "response_time_mins": None,
            "days_ago": 0,
            "fire_type": FireType.INDUSTRIAL,
            "risk_level": RiskLevel.EXTREME,
        },
        {
            "title": "Kitchen Fire in Koramangala Apartment",
            "description": "Small kitchen fire in a 2BHK apartment on the 5th floor caused by unattended cooking oil. Fire was contained to the kitchen area. One person suffered minor burns on the hand. Neighbors alerted by smoke alarm.",
            "latitude": 12.9352,
            "longitude": 77.6245,
            "address": "Flat 502, Prestige Oasis, 4th Block, Koramangala, Bangalore, Karnataka 560034",
            "severity": 2,
            "status": IncidentStatus.RESOLVED.value,
            "assigned_team": "Bangalore Fire Station - Koramangala",
            "response_time_mins": 12.3,
            "days_ago": 3,
            "fire_type": FireType.KITCHEN,
            "risk_level": RiskLevel.LOW,
        },
        {
            "title": "Electrical Fire at T. Nagar Shopping Complex",
            "description": "Electrical short circuit caused fire in a shopping complex in T. Nagar. Fire started from the main electrical panel in the basement. Entire complex evacuated. Power supply to the block cut off. Three shops on ground floor damaged.",
            "latitude": 13.0418,
            "longitude": 80.2341,
            "address": "Pondy Bazaar, T. Nagar, Chennai, Tamil Nadu 600017",
            "severity": 4,
            "status": IncidentStatus.RESOLVED.value,
            "assigned_team": "Chennai Fire & Rescue - T. Nagar",
            "response_time_mins": 10.7,
            "days_ago": 5,
            "fire_type": FireType.ELECTRICAL,
            "risk_level": RiskLevel.HIGH,
        },
        {
            "title": "Slum Fire in Dharavi Area",
            "description": "Massive fire engulfed several shanties in Dharavi slum area. The closely packed structures made it difficult for fire engines to access. Over 200 families affected. Cause suspected to be illegal electrical connections. Strong winds spreading the fire rapidly.",
            "latitude": 19.0438,
            "longitude": 72.8534,
            "address": "Dharavi Main Road, Dharavi, Mumbai, Maharashtra 400017",
            "severity": 5,
            "status": IncidentStatus.ASSIGNED.value,
            "assigned_team": "Mumbai Fire Brigade - Sion Station",
            "response_time_mins": None,
            "days_ago": 0,
            "fire_type": FireType.BUILDING,
            "risk_level": RiskLevel.EXTREME,
        },
        {
            "title": "Forest Fire near Bandipur National Park",
            "description": "Forest fire spotted in the buffer zone near Bandipur National Park. Dry vegetation and strong summer winds fueling the spread. Wildlife at risk. Forest department and fire services coordinating response. Approximately 5 hectares affected so far.",
            "latitude": 11.6720,
            "longitude": 76.6336,
            "address": "Bandipur Tiger Reserve Buffer Zone, Gundlupet, Karnataka 571111",
            "severity": 4,
            "status": IncidentStatus.EN_ROUTE.value,
            "assigned_team": "Karnataka Forest Fire Squad",
            "response_time_mins": None,
            "days_ago": 2,
            "fire_type": FireType.FOREST,
            "risk_level": RiskLevel.HIGH,
        },
        {
            "title": "Vehicle Fire on NH-48 Highway",
            "description": "A loaded goods truck caught fire on National Highway 48 near Pune. The truck was carrying textile materials which are highly flammable. Traffic backed up for 3 km on both sides. Driver escaped with minor injuries.",
            "latitude": 18.5913,
            "longitude": 73.7389,
            "address": "NH-48, near Chandni Chowk Flyover, Pune, Maharashtra 411001",
            "severity": 3,
            "status": IncidentStatus.RESOLVED.value,
            "assigned_team": "Pune Fire Brigade - Highway Unit",
            "response_time_mins": 15.2,
            "days_ago": 7,
            "fire_type": FireType.VEHICLE,
            "risk_level": RiskLevel.MODERATE,
        },
        {
            "title": "Gas Leak Fire in Salt Lake IT Park",
            "description": "Gas pipeline leak led to a small fire in the cafeteria area of an IT park building in Salt Lake Sector V. Building evacuated immediately following safety protocols. Gas supply shut off. No casualties reported but 5 employees treated for smoke inhalation.",
            "latitude": 22.5726,
            "longitude": 88.4312,
            "address": "Block EP, Sector V, Salt Lake City, Kolkata, West Bengal 700091",
            "severity": 3,
            "status": IncidentStatus.RESOLVED.value,
            "assigned_team": "Kolkata Fire Brigade - Salt Lake",
            "response_time_mins": 9.8,
            "days_ago": 10,
            "fire_type": FireType.GAS_LEAK,
            "risk_level": RiskLevel.HIGH,
        },
        {
            "title": "Warehouse Fire in Secunderabad",
            "description": "A large warehouse storing electronic goods caught fire in Secunderabad industrial area. The fire started late at night and spread rapidly. Four warehouse units completely gutted. Estimated loss of Rs 5 crore worth of inventory. Fire fighting operations went on for 6 hours.",
            "latitude": 17.4399,
            "longitude": 78.4983,
            "address": "Industrial Area, RTC X Roads, Secunderabad, Hyderabad, Telangana 500003",
            "severity": 4,
            "status": IncidentStatus.RESOLVED.value,
            "assigned_team": "Hyderabad Fire Services - Secunderabad",
            "response_time_mins": 11.5,
            "days_ago": 12,
            "fire_type": FireType.BUILDING,
            "risk_level": RiskLevel.HIGH,
        },
        {
            "title": "Electrical Fire in Jaipur Heritage Market",
            "description": "Electrical fire erupted in a heritage market building in Johari Bazaar area. Old wiring in the decades-old structure caused the fire. Precious jewelry shops at risk. Heritage structure damage concerns raised. Area has narrow lanes making firefighting challenging.",
            "latitude": 26.9157,
            "longitude": 75.8236,
            "address": "Johari Bazaar, Pink City, Jaipur, Rajasthan 302003",
            "severity": 4,
            "status": IncidentStatus.ACKNOWLEDGED.value,
            "assigned_team": "Jaipur Fire Station - Walled City",
            "response_time_mins": None,
            "days_ago": 1,
            "fire_type": FireType.ELECTRICAL,
            "risk_level": RiskLevel.HIGH,
        },
        {
            "title": "Chemical Fire at Lucknow Plastic Factory",
            "description": "Fire broke out at a plastic manufacturing unit in Amausi industrial area. Toxic fumes from burning plastic spreading to nearby residential colonies. Residents advised to stay indoors and keep windows closed. Three fire engines deployed. Factory did not have proper fire safety measures.",
            "latitude": 26.7606,
            "longitude": 80.8835,
            "address": "Plot 23, Amausi Industrial Area, Lucknow, Uttar Pradesh 226008",
            "severity": 4,
            "status": IncidentStatus.ARRIVED.value,
            "assigned_team": "Lucknow Fire Service - Amausi",
            "response_time_mins": 14.2,
            "days_ago": 4,
            "fire_type": FireType.CHEMICAL,
            "risk_level": RiskLevel.CRITICAL,
        },
        {
            "title": "Kitchen Fire at South Delhi Restaurant",
            "description": "Fire started in the kitchen of a popular restaurant in Greater Kailash due to an LPG cylinder leakage. Kitchen staff suffered burns. Restaurant was packed during dinner hours. All customers evacuated safely within 3 minutes.",
            "latitude": 28.5494,
            "longitude": 77.2430,
            "address": "M-Block Market, Greater Kailash II, New Delhi, Delhi 110048",
            "severity": 3,
            "status": IncidentStatus.RESOLVED.value,
            "assigned_team": "Delhi Fire Station - Greater Kailash",
            "response_time_mins": 7.8,
            "days_ago": 15,
            "fire_type": FireType.KITCHEN,
            "risk_level": RiskLevel.MODERATE,
        },
        {
            "title": "Building Fire in Ahmedabad Old City",
            "description": "A 4-storey residential building in the old city area caught fire. The fire started from a ground-floor garment workshop. 12 families living in the building were trapped initially. Rescue operations ongoing with 3 people rescued from the terrace by ladder.",
            "latitude": 23.0258,
            "longitude": 72.5873,
            "address": "Kalupur, Old City, Ahmedabad, Gujarat 380001",
            "severity": 5,
            "status": IncidentStatus.ARRIVED.value,
            "assigned_team": "Ahmedabad Fire & Emergency - Kalupur",
            "response_time_mins": 9.1,
            "days_ago": 2,
            "fire_type": FireType.BUILDING,
            "risk_level": RiskLevel.CRITICAL,
        },
        {
            "title": "Minor Electrical Fire at Whitefield Office",
            "description": "Small fire caused by a faulty UPS battery unit in an office building in Whitefield. Fire detected early by smoke detectors. Building maintenance team used fire extinguishers before fire department arrived. Minimal damage.",
            "latitude": 12.9698,
            "longitude": 77.7500,
            "address": "ITPL Main Road, Whitefield, Bangalore, Karnataka 560066",
            "severity": 1,
            "status": IncidentStatus.RESOLVED.value,
            "assigned_team": "Bangalore Fire Station - Whitefield",
            "response_time_mins": 18.5,
            "days_ago": 20,
            "fire_type": FireType.ELECTRICAL,
            "risk_level": RiskLevel.LOW,
        },
        {
            "title": "Vehicle Fire at Hinjawadi IT Park Parking",
            "description": "A parked car caught fire in the multi-level parking of an IT park in Hinjawadi. Fire spread to two adjacent vehicles before being contained. Suspected cause is electrical short circuit in the car's battery. Parking level evacuated.",
            "latitude": 18.5912,
            "longitude": 73.7380,
            "address": "Rajiv Gandhi Infotech Park, Phase 1, Hinjawadi, Pune, Maharashtra 411057",
            "severity": 2,
            "status": IncidentStatus.RESOLVED.value,
            "assigned_team": "Pune Fire Brigade - Hinjawadi",
            "response_time_mins": 13.0,
            "days_ago": 8,
            "fire_type": FireType.VEHICLE,
            "risk_level": RiskLevel.MODERATE,
        },
        {
            "title": "Forest Fire in Uttarakhand Hills",
            "description": "Wildfire reported in the pine forests near Nainital. Extremely dry conditions and strong mountain winds making containment difficult. Fire line extending over 2 km. NDRF teams called in for support. Several villages in the path issued evacuation warnings.",
            "latitude": 29.3803,
            "longitude": 79.4636,
            "address": "Pine Forest Area, near Nainital, Uttarakhand 263001",
            "severity": 5,
            "status": IncidentStatus.EN_ROUTE.value,
            "assigned_team": "Uttarakhand Forest Fire Service + NDRF",
            "response_time_mins": None,
            "days_ago": 0,
            "fire_type": FireType.FOREST,
            "risk_level": RiskLevel.EXTREME,
        },
        {
            "title": "Godown Fire in Howrah Industrial Belt",
            "description": "Fire broke out in a jute godown in Howrah industrial area. The highly flammable raw jute material caused the fire to spread rapidly. Four godowns in the complex affected. No casualties but huge economic loss estimated at Rs 10 crore.",
            "latitude": 22.5958,
            "longitude": 88.2636,
            "address": "Belur Industrial Area, Howrah, West Bengal 711202",
            "severity": 4,
            "status": IncidentStatus.RESOLVED.value,
            "assigned_team": "Howrah Fire Brigade - Belur",
            "response_time_mins": 16.3,
            "days_ago": 18,
            "fire_type": FireType.INDUSTRIAL,
            "risk_level": RiskLevel.HIGH,
        },
        {
            "title": "Gas Cylinder Explosion in Hyderabad Home",
            "description": "LPG cylinder exploded in a residential house in Tolichowki area. The blast damaged the kitchen and one bedroom wall. Two family members hospitalized with burn injuries. Neighbors reported hearing a loud blast. Fire contained to single house.",
            "latitude": 17.3950,
            "longitude": 78.4086,
            "address": "Tolichowki Main Road, Tolichowki, Hyderabad, Telangana 500008",
            "severity": 3,
            "status": IncidentStatus.RESOLVED.value,
            "assigned_team": "Hyderabad Fire Services - Mehdipatnam",
            "response_time_mins": 8.2,
            "days_ago": 6,
            "fire_type": FireType.GAS_LEAK,
            "risk_level": RiskLevel.HIGH,
        },
    ]

    for i, inc in enumerate(sample_incidents):
        incident_id = generate_uuid()
        created_at = now - timedelta(days=inc["days_ago"], hours=random.randint(0, 23), minutes=random.randint(0, 59))

        ai_analysis = AIAnalysis(
            severity_score=round(inc["severity"] * 1.8 + random.uniform(-0.5, 0.5), 1),
            fire_type=inc["fire_type"],
            risk_level=inc["risk_level"],
            estimated_affected_area=f"{random.randint(20, 5000)} sq meters",
            recommended_units=max(1, inc["severity"] + random.randint(-1, 2)),
            analysis_text=f"AI Analysis: {inc['description'][:100]}... Based on the reported severity of {inc['severity']}/5, "
                          f"this {inc['fire_type'].value.replace('_', ' ')} incident is classified as {inc['risk_level'].value} risk. "
                          f"Immediate response recommended with {max(1, inc['severity'] + 1)} fire units.",
            confidence_score=round(random.uniform(0.75, 0.98), 2),
            recommended_actions=[
                "Deploy fire engines immediately",
                "Evacuate nearby residents",
                "Set up emergency medical camp",
                "Coordinate with local police for traffic management",
            ],
        )

        inc_dict = {
            "id": incident_id,
            "user_id": citizen_user_id,
            "title": inc["title"],
            "description": inc["description"],
            "latitude": inc["latitude"],
            "longitude": inc["longitude"],
            "address": inc["address"],
            "severity": inc["severity"],
            "status": inc["status"],
            "media_urls": [],
            "ai_analysis": ai_analysis.model_dump(),
            "assigned_team": inc["assigned_team"],
            "created_at": created_at,
            "updated_at": created_at + timedelta(minutes=random.randint(5, 60)),
            "response_time_mins": inc["response_time_mins"],
            "reporter_name": "Aarav Sharma",
        }

        _incidents_db[incident_id] = inc_dict
