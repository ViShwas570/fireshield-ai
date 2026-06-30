# FireShield AI — API Documentation

## Base URL

```
http://localhost:8000
```

## Authentication

All protected endpoints require a JWT token in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

---

## Endpoints

### 1. Authentication

#### POST `/api/auth/register`

Register a new user account.

**Request Body:**
```json
{
  "name": "Rahul Sharma",
  "email": "rahul@example.com",
  "phone": "+91-9876543210",
  "password": "securepass123"
}
```

**Response (201):**
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "name": "Rahul Sharma",
  "email": "rahul@example.com",
  "phone": "+91-9876543210",
  "role": "citizen",
  "avatar_url": null,
  "created_at": "2025-06-20T14:22:00Z",
  "access_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

---

#### POST `/api/auth/login`

Authenticate and receive a JWT token.

**Request Body:**
```json
{
  "email": "citizen@demo.com",
  "password": "demo123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": "demo-citizen-001",
    "name": "Demo Citizen",
    "email": "citizen@demo.com",
    "role": "citizen"
  }
}
```

**Error (401):**
```json
{
  "detail": "Invalid email or password"
}
```

---

#### GET `/api/auth/profile`

Get the current authenticated user's profile.

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
{
  "id": "demo-citizen-001",
  "name": "Demo Citizen",
  "email": "citizen@demo.com",
  "phone": "+91-9876543210",
  "role": "citizen",
  "avatar_url": null,
  "created_at": "2025-01-01T00:00:00Z"
}
```

---

### 2. Incidents

#### POST `/api/incidents`

Report a new fire incident.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "title": "Building Fire at MG Road",
  "description": "Large fire spotted on the 3rd floor of the commercial complex. Smoke visible from outside.",
  "latitude": 12.9716,
  "longitude": 77.5946,
  "address": "MG Road Commercial Complex, Bangalore",
  "category": "building",
  "media_urls": ["https://example.com/photo1.jpg"]
}
```

**Response (201):**
```json
{
  "id": "inc-uuid-123",
  "user_id": "demo-citizen-001",
  "title": "Building Fire at MG Road",
  "description": "Large fire spotted on 3rd floor...",
  "latitude": 12.9716,
  "longitude": 77.5946,
  "address": "MG Road Commercial Complex, Bangalore",
  "severity": 0,
  "status": "reported",
  "media_urls": ["https://example.com/photo1.jpg"],
  "ai_analysis": null,
  "assigned_team": null,
  "created_at": "2025-06-20T14:22:00Z",
  "updated_at": "2025-06-20T14:22:00Z",
  "response_time_mins": null
}
```

---

#### GET `/api/incidents`

List all incidents with optional filters.

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| status | string | Filter by status |
| severity | int | Filter by severity (1-5) |
| search | string | Search in title/description |
| city | string | Filter by city |
| limit | int | Max results (default: 50) |
| offset | int | Pagination offset |

**Response (200):**
```json
{
  "incidents": [
    {
      "id": "inc-001",
      "title": "Factory Fire in Industrial Area",
      "severity": 5,
      "status": "en_route",
      "address": "MIDC Industrial Area, Pune",
      "created_at": "2025-06-20T14:00:00Z"
    }
  ],
  "total": 20,
  "limit": 50,
  "offset": 0
}
```

---

#### GET `/api/incidents/{id}`

Get detailed incident information.

**Response (200):** Full incident object with AI analysis and status history.

---

#### PUT `/api/incidents/{id}/status`

Update incident status (officials only).

**Request Body:**
```json
{
  "status": "assigned",
  "assigned_team": "Alpha Team",
  "notes": "2 fire engines dispatched"
}
```

**Response (200):** Updated incident object.

---

#### POST `/api/incidents/{id}/analyze`

Run AI severity analysis on an incident.

**Response (200):**
```json
{
  "severity_score": 4.2,
  "fire_type": "Commercial Building Fire",
  "risk_level": "HIGH",
  "estimated_affected_area": "500 sq meters",
  "recommended_units": 4,
  "analysis_text": "High-severity commercial building fire detected...",
  "confidence_score": 0.87
}
```

---

### 3. Emergency

#### POST `/api/emergency/sos`

Trigger an emergency SOS alert. Creates an incident, runs AI analysis, and notifies nearby stations.

**Request Body:**
```json
{
  "latitude": 12.9716,
  "longitude": 77.5946,
  "description": "Fire in my building, 3rd floor, people trapped",
  "media_urls": []
}
```

**Response (200):**
```json
{
  "incident_id": "inc-sos-001",
  "severity": 4,
  "ai_analysis": { ... },
  "nearest_station": {
    "name": "Bangalore Central Fire Station",
    "distance_km": 2.3,
    "phone": "+91-80-22212121"
  },
  "notifications_sent": 3,
  "message": "SOS received. Emergency services have been notified."
}
```

---

### 4. Nearby Services

#### GET `/api/nearby/fire-stations`

Find nearby fire stations.

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| lat | float | Yes | Latitude |
| lng | float | Yes | Longitude |
| radius | float | No | Radius in km (default: 10) |

**Response (200):**
```json
[
  {
    "id": "station-001",
    "name": "Bangalore Central Fire Station",
    "latitude": 12.9784,
    "longitude": 77.5719,
    "address": "Corporation Circle, Bangalore",
    "phone": "+91-80-22212121",
    "distance_km": 2.3,
    "available_units": 5
  }
]
```

#### GET `/api/nearby/hospitals`

Same format as fire stations, with `has_burn_unit` field.

#### GET `/api/nearby/police`

Same format as fire stations.

---

### 5. Chatbot

#### POST `/api/chatbot/message`

Send a message to the emergency chatbot.

**Request Body:**
```json
{
  "message": "How do I evacuate during a building fire?",
  "lang": "en"
}
```

**Response (200):**
```json
{
  "response": "During a building fire, follow these evacuation steps:\n\n1. **Stay calm** and alert others.\n2. **Feel the door** before opening — if hot, do NOT open.\n3. **Stay low** to avoid smoke inhalation.\n4. **Use stairs**, never elevators.\n5. **Cover nose and mouth** with a wet cloth.\n6. **Go to the nearest exit** and proceed to the assembly point.\n7. **Call 101** once you are safe.\n\n⚠️ If trapped, seal door gaps with wet cloth and signal from a window.",
  "suggestions": [
    "First aid for burns",
    "Smoke inhalation treatment",
    "What if I'm trapped?",
    "Help for children/elderly"
  ],
  "emergency_type": "evacuation"
}
```

---

### 6. Analytics

#### GET `/api/analytics/summary`

Get dashboard summary metrics.

**Response (200):**
```json
{
  "total_incidents": 156,
  "active_incidents": 12,
  "resolved_today": 8,
  "avg_response_time_mins": 7.3,
  "incidents_by_severity": {
    "1": 25, "2": 38, "3": 45, "4": 32, "5": 16
  },
  "incidents_by_status": {
    "reported": 3,
    "acknowledged": 2,
    "assigned": 3,
    "en_route": 2,
    "arrived": 2,
    "resolved": 144
  },
  "monthly_trend": [
    {"month": "Jan", "count": 22},
    {"month": "Feb", "count": 18},
    {"month": "Mar", "count": 25}
  ]
}
```

#### GET `/api/analytics/heatmap`

Get geographic heatmap data points.

**Response (200):**
```json
{
  "points": [
    {"latitude": 28.6139, "longitude": 77.2090, "intensity": 0.8},
    {"latitude": 19.0760, "longitude": 72.8777, "intensity": 0.6}
  ]
}
```

#### GET `/api/analytics/timeline`

Get recent event timeline.

**Response (200):**
```json
{
  "events": [
    {
      "id": "evt-001",
      "type": "incident_created",
      "title": "New Fire Reported",
      "description": "Building fire at MG Road, Bangalore",
      "severity": 4,
      "timestamp": "2025-06-20T14:22:00Z"
    }
  ]
}
```

---

### 7. WebSocket

#### WS `/ws/incidents`

Connect to receive real-time incident updates.

**Messages Received:**
```json
{
  "type": "new_incident",
  "data": { /* incident object */ }
}
```

```json
{
  "type": "status_update",
  "data": {
    "incident_id": "inc-001",
    "old_status": "reported",
    "new_status": "assigned",
    "assigned_team": "Alpha Team"
  }
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

| Status Code | Meaning |
|-------------|---------|
| 400 | Bad Request — Invalid input |
| 401 | Unauthorized — Missing or invalid token |
| 403 | Forbidden — Insufficient permissions |
| 404 | Not Found — Resource doesn't exist |
| 422 | Validation Error — Invalid request body |
| 500 | Internal Server Error |

---

## Rate Limits

| Endpoint | Limit |
|----------|-------|
| Auth endpoints | 10 requests/minute |
| SOS endpoint | 5 requests/minute |
| All others | 60 requests/minute |

> Note: Rate limiting is not enforced in the demo version.
