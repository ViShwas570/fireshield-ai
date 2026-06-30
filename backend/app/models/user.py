"""
FireShield AI - User Models

Pydantic models for user registration, authentication, and profile management.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    """User roles in the FireShield system."""
    CITIZEN = "citizen"
    OFFICIAL = "official"
    ADMIN = "admin"


class UserCreate(BaseModel):
    """Schema for user registration."""
    name: str = Field(..., min_length=2, max_length=100, description="Full name of the user")
    email: str = Field(..., description="Email address")
    phone: str = Field(..., min_length=10, max_length=15, description="Phone number")
    password: str = Field(..., min_length=6, description="Password (min 6 characters)")
    role: UserRole = Field(default=UserRole.CITIZEN, description="User role")


class UserLogin(BaseModel):
    """Schema for user login."""
    email: str = Field(..., description="Email address")
    password: str = Field(..., description="Password")


class UserResponse(BaseModel):
    """Schema for user data in API responses."""
    id: str = Field(..., description="Unique user identifier (UUID)")
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    phone: str = Field(..., description="Phone number")
    avatar_url: Optional[str] = Field(None, description="Profile picture URL")
    role: UserRole = Field(..., description="User role")
    created_at: datetime = Field(..., description="Account creation timestamp")


class UserProfile(BaseModel):
    """Schema for updating user profile."""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    avatar_url: Optional[str] = None


class TokenResponse(BaseModel):
    """Schema for authentication token response."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    user: UserResponse = Field(..., description="Authenticated user data")


class UserInDB(BaseModel):
    """Internal user model with hashed password (not exposed via API)."""
    id: str
    name: str
    email: str
    phone: str
    avatar_url: Optional[str] = None
    role: UserRole
    hashed_password: str
    created_at: datetime
