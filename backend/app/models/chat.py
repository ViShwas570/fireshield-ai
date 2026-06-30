"""
FireShield AI - Chat Models

Pydantic models for the emergency chatbot system.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class EmergencyType(str, Enum):
    """Types of emergency situations the chatbot can address."""
    FIRE_EVACUATION = "fire_evacuation"
    BURN_FIRST_AID = "burn_first_aid"
    SMOKE_INHALATION = "smoke_inhalation"
    ELECTRICAL_FIRE = "electrical_fire"
    GAS_LEAK = "gas_leak"
    CHILD_ELDERLY_EVACUATION = "child_elderly_evacuation"
    PET_EVACUATION = "pet_evacuation"
    FIRE_SAFETY = "fire_safety"
    GENERAL = "general"


class ChatMessage(BaseModel):
    """Schema for incoming chat messages."""
    message: str = Field(..., min_length=1, max_length=1000, description="User's chat message")
    lang: str = Field(default="en", description="Language: 'en' for English, 'hi' for Hindi")
    context: Optional[str] = Field(None, description="Previous conversation context")


class ChatResponse(BaseModel):
    """Schema for chatbot responses."""
    response: str = Field(..., description="Chatbot's response text")
    suggestions: List[str] = Field(default_factory=list, description="Quick reply suggestions")
    emergency_type: Optional[EmergencyType] = Field(None, description="Detected emergency type")
    is_emergency: bool = Field(default=False, description="Whether this is a critical emergency")
    emergency_number: Optional[str] = Field(None, description="Relevant emergency phone number")
