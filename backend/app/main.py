"""
FireShield AI — FastAPI Main Application
AI-Powered Emergency Response System for India
"""
from fastapi import FastAPI, HTTPException, Depends, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, List
import json

from app.config import settings
from app.models.schemas import (
    UserCreate, UserLogin, UserResponse, LoginResponse,
    IncidentCreate, IncidentResponse, IncidentStatusUpdate, IncidentListResponse,
    SOSRequest, NearbyService, ChatRequest, ChatResponse,
    DashboardSummary, HeatmapPoint, TimelineEvent, AIAnalysis,
)
from app.services.engine import (
    register_user, authenticate_user, verify_token, get_user_response,
    create_incident, list_incidents, get_incident, update_incident_status,
    run_analysis_on_incident, get_chat_response, find_nearby,
    send_sos_notification, get_dashboard_summary, get_heatmap_data, get_timeline,
    seed_demo_data, ws_clients, analyze_fire_severity,
)

# ─── App Initialization ──────────────────────────────────
app = FastAPI(
    title="🔥 FireShield AI API",
    description="AI-Powered Emergency Response System — Protecting India from Fire Emergencies",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer(auto_error=False)

# ─── Auth Dependency ──────────────────────────────────────
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(status_code=401, detail="Authentication required")
    user = verify_token(credentials.credentials)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user

async def optional_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials:
        return verify_token(credentials.credentials)
    return None

# ─── Startup ──────────────────────────────────────────────
@app.on_event("startup")
async def startup():
    seed_demo_data()
    print("🔥 FireShield AI API started — Demo data seeded")

# ─── Root ─────────────────────────────────────────────────
@app.get("/", tags=["System"])
async def root():
    return {
        "name": "🔥 FireShield AI API",
        "version": "1.0.0",
        "status": "operational",
        "description": "AI-Powered Emergency Response System",
        "docs": "/docs",
        "endpoints": {
            "auth": "/api/auth",
            "incidents": "/api/incidents",
            "emergency": "/api/emergency",
            "nearby": "/api/nearby",
            "chatbot": "/api/chatbot",
            "analytics": "/api/analytics",
            "websocket": "/ws/incidents"
        }
    }

@app.get("/health", tags=["System"])
async def health():
    return {"status": "healthy", "service": "fireshield-ai"}

# ═══════════════════════════════════════════════════════════
# AUTH ROUTES
# ═══════════════════════════════════════════════════════════
@app.post("/api/auth/register", response_model=LoginResponse, tags=["Auth"])
async def api_register(data: UserCreate):
    try:
        return register_user(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/auth/login", response_model=LoginResponse, tags=["Auth"])
async def api_login(data: UserLogin):
    try:
        return authenticate_user(data.email, data.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@app.get("/api/auth/profile", response_model=UserResponse, tags=["Auth"])
async def api_profile(user=Depends(get_current_user)):
    return get_user_response(user)

# ═══════════════════════════════════════════════════════════
# INCIDENT ROUTES
# ═══════════════════════════════════════════════════════════
@app.post("/api/incidents", response_model=IncidentResponse, status_code=201, tags=["Incidents"])
async def api_create_incident(data: IncidentCreate, user=Depends(get_current_user)):
    inc = create_incident(data, user["id"])
    await broadcast_ws({"type": "new_incident", "data": inc.model_dump()})
    return inc

@app.get("/api/incidents", response_model=IncidentListResponse, tags=["Incidents"])
async def api_list_incidents(
    status: Optional[str] = None,
    severity: Optional[int] = None,
    search: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    items, total = list_incidents(status, severity, search, limit, offset)
    return IncidentListResponse(incidents=items, total=total)

@app.get("/api/incidents/{incident_id}", response_model=IncidentResponse, tags=["Incidents"])
async def api_get_incident(incident_id: str):
    inc = get_incident(incident_id)
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")
    return inc

@app.put("/api/incidents/{incident_id}/status", response_model=IncidentResponse, tags=["Incidents"])
async def api_update_status(incident_id: str, data: IncidentStatusUpdate):
    inc = update_incident_status(incident_id, data.status, data.assigned_team, data.notes)
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")
    await broadcast_ws({"type": "status_update", "data": {"incident_id": incident_id, "new_status": data.status, "assigned_team": data.assigned_team}})
    return inc

@app.post("/api/incidents/{incident_id}/analyze", response_model=AIAnalysis, tags=["Incidents"])
async def api_analyze_incident(incident_id: str):
    analysis = run_analysis_on_incident(incident_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Incident not found")
    return analysis

# ═══════════════════════════════════════════════════════════
# EMERGENCY SOS
# ═══════════════════════════════════════════════════════════
@app.post("/api/emergency/sos", tags=["Emergency"])
async def api_sos(data: SOSRequest, user=Depends(optional_user)):
    uid = user["id"] if user else "anonymous"
    inc_data = IncidentCreate(
        title=f"🚨 SOS Emergency Report",
        description=data.description,
        latitude=data.latitude, longitude=data.longitude,
        address="SOS Location", category="other",
        media_urls=data.media_urls)
    inc = create_incident(inc_data, uid)

    analysis = run_analysis_on_incident(inc.id)
    notified = send_sos_notification(inc.id, data.latitude, data.longitude)
    stations = find_nearby(data.latitude, data.longitude, "fire_station", 20)

    await broadcast_ws({"type": "sos_alert", "data": inc.model_dump()})

    return {
        "incident_id": inc.id,
        "severity": analysis.severity_score if analysis else 0,
        "ai_analysis": analysis.model_dump() if analysis else None,
        "nearest_station": stations[0].model_dump() if stations else None,
        "notifications_sent": notified,
        "message": "🚨 SOS received! Emergency services have been notified. Stay safe."
    }

# ═══════════════════════════════════════════════════════════
# NEARBY SERVICES
# ═══════════════════════════════════════════════════════════
@app.get("/api/nearby/fire-stations", response_model=List[NearbyService], tags=["Nearby Services"])
async def api_nearby_fire_stations(lat: float, lng: float, radius: float = 15.0):
    return find_nearby(lat, lng, "fire_station", radius)

@app.get("/api/nearby/hospitals", response_model=List[NearbyService], tags=["Nearby Services"])
async def api_nearby_hospitals(lat: float, lng: float, radius: float = 15.0):
    return find_nearby(lat, lng, "hospital", radius)

@app.get("/api/nearby/police", response_model=List[NearbyService], tags=["Nearby Services"])
async def api_nearby_police(lat: float, lng: float, radius: float = 15.0):
    return find_nearby(lat, lng, "police", radius)

# ═══════════════════════════════════════════════════════════
# CHATBOT
# ═══════════════════════════════════════════════════════════
@app.post("/api/chatbot/message", response_model=ChatResponse, tags=["Chatbot"])
async def api_chatbot(data: ChatRequest):
    return get_chat_response(data.message, data.lang)

# ═══════════════════════════════════════════════════════════
# ANALYTICS
# ═══════════════════════════════════════════════════════════
@app.get("/api/analytics/summary", response_model=DashboardSummary, tags=["Analytics"])
async def api_analytics_summary():
    return get_dashboard_summary()

@app.get("/api/analytics/heatmap", tags=["Analytics"])
async def api_analytics_heatmap():
    return {"points": [p.model_dump() for p in get_heatmap_data()]}

@app.get("/api/analytics/timeline", tags=["Analytics"])
async def api_analytics_timeline():
    return {"events": [e.model_dump() for e in get_timeline()]}

# ═══════════════════════════════════════════════════════════
# WEBSOCKET
# ═══════════════════════════════════════════════════════════
async def broadcast_ws(message: dict):
    dead = []
    for ws in ws_clients:
        try:
            await ws.send_text(json.dumps(message, default=str))
        except Exception:
            dead.append(ws)
    for ws in dead:
        ws_clients.remove(ws)

@app.websocket("/ws/incidents")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    ws_clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo back for keep-alive
            await websocket.send_text(json.dumps({"type": "pong"}))
    except WebSocketDisconnect:
        if websocket in ws_clients:
            ws_clients.remove(websocket)
