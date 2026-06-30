"""
FireShield AI - Authentication Service

Handles user registration, authentication, JWT token management,
and pre-seeds demo users for development.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings
from app.models.user import (
    UserCreate, UserLogin, UserResponse, TokenResponse, UserInDB, UserRole,
)
from app.utils.helpers import generate_uuid, now_utc


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer token scheme
security = HTTPBearer()

# In-memory user store: email -> UserInDB
_users_db: Dict[str, UserInDB] = {}

# Index by ID for quick lookup
_users_by_id: Dict[str, UserInDB] = {}


def _hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    return pwd_context.hash(password)


def _verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a bcrypt hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Payload data to encode in the token.
        expires_delta: Optional custom expiration time.

    Returns:
        Encoded JWT string.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def register_user(user_data: UserCreate) -> TokenResponse:
    """
    Register a new user.

    Args:
        user_data: User registration data.

    Returns:
        TokenResponse with JWT token and user data.

    Raises:
        HTTPException: If email is already registered.
    """
    if user_data.email.lower() in _users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user_id = generate_uuid()
    user_in_db = UserInDB(
        id=user_id,
        name=user_data.name,
        email=user_data.email.lower(),
        phone=user_data.phone,
        role=user_data.role,
        hashed_password=_hash_password(user_data.password),
        created_at=now_utc(),
    )

    _users_db[user_in_db.email] = user_in_db
    _users_by_id[user_id] = user_in_db

    token = create_access_token({"sub": user_id, "email": user_in_db.email, "role": user_in_db.role.value})

    user_response = UserResponse(
        id=user_in_db.id,
        name=user_in_db.name,
        email=user_in_db.email,
        phone=user_in_db.phone,
        avatar_url=user_in_db.avatar_url,
        role=user_in_db.role,
        created_at=user_in_db.created_at,
    )

    return TokenResponse(access_token=token, user=user_response)


def authenticate_user(login_data: UserLogin) -> TokenResponse:
    """
    Authenticate a user with email and password.

    Args:
        login_data: Login credentials.

    Returns:
        TokenResponse with JWT token and user data.

    Raises:
        HTTPException: If credentials are invalid.
    """
    email = login_data.email.lower()
    user = _users_db.get(email)

    if not user or not _verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token({"sub": user.id, "email": user.email, "role": user.role.value})

    user_response = UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        phone=user.phone,
        avatar_url=user.avatar_url,
        role=user.role,
        created_at=user.created_at,
    )

    return TokenResponse(access_token=token, user=user_response)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> UserResponse:
    """
    Dependency to extract and validate the current user from a JWT token.

    Args:
        credentials: Bearer token from the Authorization header.

    Returns:
        UserResponse for the authenticated user.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            credentials.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = _users_by_id.get(user_id)
    if user is None:
        raise credentials_exception

    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        phone=user.phone,
        avatar_url=user.avatar_url,
        role=user.role,
        created_at=user.created_at,
    )


def get_user_by_id(user_id: str) -> Optional[UserInDB]:
    """
    Retrieve a user by their ID.

    Args:
        user_id: The user's UUID.

    Returns:
        UserInDB if found, None otherwise.
    """
    return _users_by_id.get(user_id)


def seed_demo_users() -> None:
    """
    Pre-seed the user store with demo users for development/testing.
    Creates three users: citizen, official, and admin.
    """
    demo_users = [
        UserCreate(
            name="Aarav Sharma",
            email="citizen@demo.com",
            phone="9876543210",
            password="demo123",
            role=UserRole.CITIZEN,
        ),
        UserCreate(
            name="Priya Patel",
            email="official@demo.com",
            phone="9876543211",
            password="demo123",
            role=UserRole.OFFICIAL,
        ),
        UserCreate(
            name="Vikram Singh",
            email="admin@demo.com",
            phone="9876543212",
            password="demo123",
            role=UserRole.ADMIN,
        ),
    ]

    for user_data in demo_users:
        if user_data.email.lower() not in _users_db:
            user_id = generate_uuid()
            user_in_db = UserInDB(
                id=user_id,
                name=user_data.name,
                email=user_data.email.lower(),
                phone=user_data.phone,
                role=user_data.role,
                hashed_password=_hash_password(user_data.password),
                created_at=now_utc(),
            )
            _users_db[user_in_db.email] = user_in_db
            _users_by_id[user_id] = user_in_db


def get_demo_user_id(role: str = "citizen") -> str:
    """
    Get the user ID for a demo user by role.

    Args:
        role: The role to look up ('citizen', 'official', 'admin').

    Returns:
        The user ID string.
    """
    email_map = {
        "citizen": "citizen@demo.com",
        "official": "official@demo.com",
        "admin": "admin@demo.com",
    }
    email = email_map.get(role, "citizen@demo.com")
    user = _users_db.get(email)
    return user.id if user else generate_uuid()
