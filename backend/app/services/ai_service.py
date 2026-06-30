"""
FireShield AI - AI Analysis Service

Simulates Gemini AI analysis for fire incidents. Classifies fire type,
assesses severity, estimates risk, and generates detailed analysis text
based on keywords in the incident description.
"""

import random
from typing import List, Optional

from app.models.incident import AIAnalysis, FireType, RiskLevel


# Keyword mappings for fire type classification
_FIRE_TYPE_KEYWORDS = {
    FireType.INDUSTRIAL: ["factory", "industrial", "warehouse", "godown", "manufacturing", "plant", "mill", "chemical"],
    FireType.BUILDING: ["building", "apartment", "flat", "floor", "storey", "tower", "complex", "residential", "office", "mall", "shanty", "slum"],
    FireType.FOREST: ["forest", "jungle", "wildfire", "vegetation", "pine", "tree", "park", "wildlife", "hill"],
    FireType.ELECTRICAL: ["electrical", "short circuit", "wiring", "transformer", "power", "cable", "panel", "ups", "battery"],
    FireType.KITCHEN: ["kitchen", "cooking", "stove", "oven", "oil", "restaurant", "cafeteria", "canteen"],
    FireType.VEHICLE: ["vehicle", "car", "truck", "bus", "auto", "scooter", "bike", "parking", "highway"],
    FireType.GAS_LEAK: ["gas", "lpg", "cylinder", "propane", "pipeline", "leak", "explosion"],
    FireType.CHEMICAL: ["chemical", "toxic", "hazardous", "plastic", "solvent", "acid", "fumes"],
}

# Severity adjustment keywords
_HIGH_SEVERITY_KEYWORDS = [
    "explosion", "trapped", "collapse", "spreading", "massive", "huge",
    "multiple", "casualties", "toxic", "hazardous", "chemical", "factory",
    "industrial", "slum", "crowded", "missing", "structural",
]

_LOW_SEVERITY_KEYWORDS = [
    "small", "minor", "contained", "extinguished", "kitchen", "single",
    "detected early", "smoke detector", "fire extinguisher", "no casualties",
    "no injuries", "minimal",
]


def _classify_fire_type(description: str) -> FireType:
    """
    Classify the fire type based on keywords in the description.

    Args:
        description: The incident description text.

    Returns:
        The classified FireType enum value.
    """
    desc_lower = description.lower()
    scores = {}

    for fire_type, keywords in _FIRE_TYPE_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in desc_lower)
        if score > 0:
            scores[fire_type] = score

    if scores:
        return max(scores, key=scores.get)
    return FireType.UNKNOWN


def _assess_risk_level(severity_score: float) -> RiskLevel:
    """
    Determine risk level from the severity score.

    Args:
        severity_score: Numeric severity (0-10).

    Returns:
        The corresponding RiskLevel.
    """
    if severity_score >= 8.5:
        return RiskLevel.EXTREME
    elif severity_score >= 7.0:
        return RiskLevel.CRITICAL
    elif severity_score >= 5.0:
        return RiskLevel.HIGH
    elif severity_score >= 3.0:
        return RiskLevel.MODERATE
    else:
        return RiskLevel.LOW


def _calculate_severity_score(description: str, base_severity: int) -> float:
    """
    Calculate a refined AI severity score based on description keywords
    and the user-reported severity.

    Args:
        description: Incident description text.
        base_severity: User-reported severity (1-5).

    Returns:
        AI severity score (0-10).
    """
    desc_lower = description.lower()
    score = base_severity * 1.6  # Scale 1-5 to roughly 1.6-8.0

    # Adjust for high-severity indicators
    high_matches = sum(1 for kw in _HIGH_SEVERITY_KEYWORDS if kw in desc_lower)
    score += high_matches * 0.3

    # Adjust for low-severity indicators
    low_matches = sum(1 for kw in _LOW_SEVERITY_KEYWORDS if kw in desc_lower)
    score -= low_matches * 0.3

    # Add slight randomness for realism
    score += random.uniform(-0.3, 0.3)

    return round(max(0.5, min(10.0, score)), 1)


def _estimate_affected_area(fire_type: FireType, severity_score: float) -> str:
    """
    Estimate the affected area based on fire type and severity.

    Args:
        fire_type: The classified fire type.
        severity_score: The AI severity score.

    Returns:
        Human-readable affected area estimate.
    """
    base_areas = {
        FireType.INDUSTRIAL: (200, 5000),
        FireType.BUILDING: (50, 2000),
        FireType.FOREST: (5000, 50000),
        FireType.ELECTRICAL: (20, 500),
        FireType.KITCHEN: (10, 50),
        FireType.VEHICLE: (10, 100),
        FireType.GAS_LEAK: (30, 300),
        FireType.CHEMICAL: (100, 3000),
        FireType.UNKNOWN: (50, 1000),
    }

    min_area, max_area = base_areas.get(fire_type, (50, 1000))
    severity_factor = severity_score / 10.0
    area = int(min_area + (max_area - min_area) * severity_factor)
    return f"{area} sq meters"


def _recommend_units(fire_type: FireType, severity_score: float) -> int:
    """
    Recommend the number of fire units to dispatch.

    Args:
        fire_type: The classified fire type.
        severity_score: The AI severity score.

    Returns:
        Recommended number of fire units.
    """
    base_units = {
        FireType.INDUSTRIAL: 4,
        FireType.BUILDING: 3,
        FireType.FOREST: 5,
        FireType.ELECTRICAL: 2,
        FireType.KITCHEN: 1,
        FireType.VEHICLE: 2,
        FireType.GAS_LEAK: 3,
        FireType.CHEMICAL: 4,
        FireType.UNKNOWN: 2,
    }

    base = base_units.get(fire_type, 2)
    severity_add = int(severity_score / 3)
    return max(1, min(10, base + severity_add))


def _generate_recommended_actions(fire_type: FireType, risk_level: RiskLevel) -> List[str]:
    """
    Generate context-specific recommended response actions.

    Args:
        fire_type: The classified fire type.
        risk_level: The assessed risk level.

    Returns:
        List of recommended action strings.
    """
    actions = ["Deploy fire engines to the incident location"]

    # Common actions
    if risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL, RiskLevel.EXTREME):
        actions.append("Evacuate all people within a 500-meter radius immediately")
        actions.append("Set up emergency medical camp near the site")
        actions.append("Request additional backup units from neighboring stations")

    if risk_level == RiskLevel.EXTREME:
        actions.append("Alert NDRF (National Disaster Response Force) for support")
        actions.append("Activate city-wide emergency response protocol")

    # Type-specific actions
    type_actions = {
        FireType.INDUSTRIAL: [
            "Check for hazardous material inventory at the facility",
            "Deploy HAZMAT team for chemical containment",
            "Monitor air quality in surrounding residential areas",
        ],
        FireType.BUILDING: [
            "Deploy aerial ladder trucks for upper floor rescue",
            "Check structural integrity before entering the building",
            "Coordinate with building management for floor plans",
        ],
        FireType.FOREST: [
            "Create firebreaks to prevent further spread",
            "Deploy helicopter for aerial water drops if available",
            "Issue evacuation warnings to nearby settlements",
            "Coordinate with Forest Department for wildlife rescue",
        ],
        FireType.ELECTRICAL: [
            "Ensure power supply is completely disconnected before approach",
            "Deploy CO2 and dry chemical extinguishers (NOT water)",
            "Contact electricity board for area power shutdown",
        ],
        FireType.KITCHEN: [
            "Use fire blankets or CO2 extinguishers for oil fires",
            "Ensure gas supply is shut off",
            "Ventilate the area after fire is contained",
        ],
        FireType.VEHICLE: [
            "Maintain safe distance due to fuel tank explosion risk",
            "Coordinate with traffic police for road closure",
            "Have foam fire extinguishers ready for fuel fires",
        ],
        FireType.GAS_LEAK: [
            "Evacuate immediately - explosion risk is high",
            "DO NOT use electrical switches near the leak area",
            "Contact gas supply company for emergency shutdown",
            "Deploy gas leak detection equipment",
        ],
        FireType.CHEMICAL: [
            "Identify chemicals involved before approaching",
            "Deploy full HAZMAT protective gear for responders",
            "Set up decontamination zone for affected individuals",
            "Monitor wind direction for toxic fume spread",
        ],
    }

    actions.extend(type_actions.get(fire_type, []))
    actions.append("Coordinate with local police for crowd control and traffic management")

    return actions


def _generate_analysis_text(
    fire_type: FireType,
    risk_level: RiskLevel,
    severity_score: float,
    affected_area: str,
    recommended_units: int,
    description: str,
) -> str:
    """
    Generate a detailed AI analysis narrative.

    Args:
        fire_type: Classified fire type.
        risk_level: Assessed risk level.
        severity_score: AI severity score.
        affected_area: Estimated affected area string.
        recommended_units: Number of recommended units.
        description: Original incident description.

    Returns:
        Detailed analysis text string.
    """
    fire_type_label = fire_type.value.replace("_", " ").title()
    risk_label = risk_level.value.upper()

    analysis = (
        f"🔥 **FireShield AI Analysis Report**\n\n"
        f"**Fire Classification:** {fire_type_label}\n"
        f"**Risk Assessment:** {risk_label}\n"
        f"**AI Severity Score:** {severity_score}/10\n"
        f"**Estimated Affected Area:** {affected_area}\n\n"
        f"**Situation Assessment:**\n"
    )

    if risk_level == RiskLevel.EXTREME:
        analysis += (
            "⚠️ EXTREME RISK - This is a critical emergency requiring maximum response. "
            "Multiple fire units, ambulances, and potentially NDRF support are recommended. "
            "Large-scale evacuation may be necessary. This incident has the potential for "
            "significant casualties and property damage if not controlled immediately.\n\n"
        )
    elif risk_level == RiskLevel.CRITICAL:
        analysis += (
            "🔴 CRITICAL RISK - Urgent response required. This incident poses serious threats "
            "to life and property. Multiple fire units should be dispatched immediately. "
            "Evacuation of nearby areas is strongly recommended. Medical teams should be "
            "on standby.\n\n"
        )
    elif risk_level == RiskLevel.HIGH:
        analysis += (
            "🟠 HIGH RISK - Swift response needed. The fire has potential to escalate if not "
            "addressed quickly. Nearby residents should be alerted. Standard fire response "
            "protocol should be followed with additional units on standby.\n\n"
        )
    elif risk_level == RiskLevel.MODERATE:
        analysis += (
            "🟡 MODERATE RISK - Standard response is appropriate. The fire appears containable "
            "with standard equipment. Monitor for escalation and have backup units ready "
            "if needed.\n\n"
        )
    else:
        analysis += (
            "🟢 LOW RISK - The situation appears manageable. Standard single-unit response "
            "should be sufficient. The fire is likely contained or easily containable. "
            "Continue monitoring.\n\n"
        )

    analysis += (
        f"**Recommended Response:** Deploy {recommended_units} fire unit(s) to the location. "
        f"Estimated affected area is {affected_area}. "
    )

    if fire_type == FireType.CHEMICAL or fire_type == FireType.INDUSTRIAL:
        analysis += "HAZMAT protocols should be activated. "
    if fire_type == FireType.GAS_LEAK:
        analysis += "Gas leak containment procedures must be followed. Explosion risk is elevated. "
    if fire_type == FireType.ELECTRICAL:
        analysis += "Power must be disconnected before firefighting operations begin. "

    analysis += (
        f"\n\n**Confidence Level:** This analysis was generated with AI-powered assessment. "
        f"On-ground verification by fire officials is essential for final decision-making."
    )

    return analysis


def analyze_fire_severity(
    description: str,
    media_urls: Optional[List[str]] = None,
    location: Optional[str] = None,
    base_severity: int = 3,
) -> AIAnalysis:
    """
    Simulate Gemini AI analysis of a fire incident.

    Analyzes the description text using keyword matching and heuristics
    to classify the fire type, assess severity and risk, estimate affected
    area, and generate a detailed analysis report.

    Args:
        description: Detailed incident description.
        media_urls: Optional list of media/image URLs (simulated analysis).
        location: Optional address/location string for context.
        base_severity: User-reported severity (1-5), defaults to 3.

    Returns:
        AIAnalysis with complete fire analysis data.
    """
    # Classify fire type from description
    fire_type = _classify_fire_type(description)

    # Calculate refined severity score
    severity_score = _calculate_severity_score(description, base_severity)

    # Assess risk level
    risk_level = _assess_risk_level(severity_score)

    # Estimate affected area
    affected_area = _estimate_affected_area(fire_type, severity_score)

    # Recommend units
    units = _recommend_units(fire_type, severity_score)

    # Generate recommended actions
    actions = _generate_recommended_actions(fire_type, risk_level)

    # Generate detailed analysis text
    analysis_text = _generate_analysis_text(
        fire_type, risk_level, severity_score, affected_area, units, description
    )

    # Calculate confidence score (higher for more keyword matches)
    desc_lower = description.lower()
    total_keyword_matches = sum(
        1
        for keywords in _FIRE_TYPE_KEYWORDS.values()
        for kw in keywords
        if kw in desc_lower
    )
    confidence = min(0.98, 0.60 + total_keyword_matches * 0.04 + random.uniform(0, 0.05))

    # Boost confidence slightly if media is provided
    if media_urls and len(media_urls) > 0:
        confidence = min(0.99, confidence + 0.05)

    return AIAnalysis(
        severity_score=severity_score,
        fire_type=fire_type,
        risk_level=risk_level,
        estimated_affected_area=affected_area,
        recommended_units=units,
        analysis_text=analysis_text,
        confidence_score=round(confidence, 2),
        recommended_actions=actions,
    )
