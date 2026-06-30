"""
FireShield AI — All Backend Services
Auth, Incidents, AI Analysis, Chatbot, Location, Notifications, Analytics
"""
from __future__ import annotations
import random, math
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from passlib.context import CryptContext
from jose import jwt
from app.config import settings
from app.utils.helpers import generate_uuid, now_iso, haversine_distance
from app.models.schemas import (
    UserCreate, UserResponse, LoginResponse, UserRole,
    IncidentCreate, IncidentResponse, IncidentStatus, AIAnalysis, StatusHistoryEntry,
    NearbyService, ChatResponse, DashboardSummary, HeatmapPoint, TimelineEvent,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ═══════════════════════════════════════════════════════════
# IN-MEMORY DATA STORES
# ═══════════════════════════════════════════════════════════
users_db: Dict[str, dict] = {}
incidents_db: Dict[str, dict] = {}
notifications_log: List[dict] = []
ws_clients: List[Any] = []

# ═══════════════════════════════════════════════════════════
# AUTH SERVICE
# ═══════════════════════════════════════════════════════════
def _create_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({**data, "exp": expire}, settings.secret_key, algorithm=settings.algorithm)

def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        uid = payload.get("sub")
        return users_db.get(uid)
    except Exception:
        return None

def register_user(data: UserCreate) -> LoginResponse:
    for u in users_db.values():
        if u["email"] == data.email:
            raise ValueError("Email already registered")
    uid = generate_uuid()
    user = {
        "id": uid, "name": data.name, "email": data.email,
        "phone": data.phone, "role": "citizen",
        "avatar_url": None, "created_at": now_iso(),
        "password_hash": pwd_context.hash(data.password),
    }
    users_db[uid] = user
    token = _create_token({"sub": uid})
    return LoginResponse(
        access_token=token,
        user=UserResponse(id=uid, name=data.name, email=data.email,
                          phone=data.phone, role=UserRole.citizen,
                          created_at=user["created_at"]))

def authenticate_user(email: str, password: str) -> LoginResponse:
    for u in users_db.values():
        if u["email"] == email and pwd_context.verify(password, u["password_hash"]):
            token = _create_token({"sub": u["id"]})
            return LoginResponse(
                access_token=token,
                user=UserResponse(id=u["id"], name=u["name"], email=u["email"],
                                  phone=u["phone"], role=UserRole(u["role"]),
                                  avatar_url=u.get("avatar_url"),
                                  created_at=u["created_at"]))
    raise ValueError("Invalid email or password")

def get_user_response(user: dict) -> UserResponse:
    return UserResponse(id=user["id"], name=user["name"], email=user["email"],
                        phone=user["phone"], role=UserRole(user["role"]),
                        avatar_url=user.get("avatar_url"), created_at=user["created_at"])

# ═══════════════════════════════════════════════════════════
# INCIDENT SERVICE
# ═══════════════════════════════════════════════════════════
def _incident_to_response(inc: dict) -> IncidentResponse:
    ai = None
    if inc.get("ai_analysis"):
        ai = AIAnalysis(**inc["ai_analysis"])
    history = [StatusHistoryEntry(**h) for h in inc.get("status_history", [])]
    return IncidentResponse(
        id=inc["id"], user_id=inc["user_id"], user_name=inc.get("user_name", ""),
        title=inc["title"], description=inc["description"],
        latitude=inc["latitude"], longitude=inc["longitude"],
        address=inc["address"], category=inc.get("category", "other"),
        severity=inc["severity"], status=inc["status"],
        media_urls=inc.get("media_urls", []),
        ai_analysis=ai, assigned_team=inc.get("assigned_team"),
        created_at=inc["created_at"], updated_at=inc["updated_at"],
        response_time_mins=inc.get("response_time_mins"),
        status_history=history)

def create_incident(data: IncidentCreate, user_id: str) -> IncidentResponse:
    iid = generate_uuid()[:8]
    ts = now_iso()
    user = users_db.get(user_id, {})
    inc = {
        "id": f"INC-{iid.upper()}", "user_id": user_id,
        "user_name": user.get("name", "Unknown"),
        "title": data.title, "description": data.description,
        "latitude": data.latitude, "longitude": data.longitude,
        "address": data.address, "category": data.category,
        "severity": 0, "status": "reported",
        "media_urls": data.media_urls, "ai_analysis": None,
        "assigned_team": None, "created_at": ts, "updated_at": ts,
        "response_time_mins": None,
        "status_history": [{"status": "reported", "timestamp": ts, "updated_by": "system"}],
    }
    incidents_db[inc["id"]] = inc
    return _incident_to_response(inc)

def list_incidents(status: str = None, severity: int = None, search: str = None,
                   limit: int = 50, offset: int = 0) -> tuple:
    items = list(incidents_db.values())
    if status:
        items = [i for i in items if i["status"] == status]
    if severity:
        items = [i for i in items if i["severity"] == severity]
    if search:
        s = search.lower()
        items = [i for i in items if s in i["title"].lower() or s in i["description"].lower() or s in i["address"].lower()]
    items.sort(key=lambda x: x["created_at"], reverse=True)
    total = len(items)
    items = items[offset:offset + limit]
    return [_incident_to_response(i) for i in items], total

def get_incident(incident_id: str) -> Optional[IncidentResponse]:
    inc = incidents_db.get(incident_id)
    return _incident_to_response(inc) if inc else None

def update_incident_status(incident_id: str, status: str,
                           assigned_team: str = None, notes: str = "") -> Optional[IncidentResponse]:
    inc = incidents_db.get(incident_id)
    if not inc:
        return None
    inc["status"] = status
    inc["updated_at"] = now_iso()
    if assigned_team:
        inc["assigned_team"] = assigned_team
    if status == "assigned" and not inc.get("response_time_mins"):
        created = datetime.fromisoformat(inc["created_at"].replace("Z", ""))
        diff = (datetime.utcnow() - created).total_seconds() / 60
        inc["response_time_mins"] = round(diff, 1)
    inc["status_history"].append({
        "status": status, "timestamp": now_iso(),
        "updated_by": "dispatcher", "notes": notes})
    return _incident_to_response(inc)

# ═══════════════════════════════════════════════════════════
# AI SERVICE (Simulated Gemini)
# ═══════════════════════════════════════════════════════════
def analyze_fire_severity(description: str, category: str = "other",
                          lat: float = 0, lng: float = 0) -> AIAnalysis:
    """Simulate Gemini AI fire severity analysis."""
    desc_lower = description.lower()
    score = 2.5
    fire_type = "General Fire"
    risk = "MODERATE"
    area = "50 sq meters"
    units = 2

    keyword_map = {
        "factory": (4.5, "Industrial/Factory Fire", "CRITICAL", "2000 sq meters", 6),
        "industrial": (4.2, "Industrial Fire", "HIGH", "1500 sq meters", 5),
        "chemical": (4.8, "Chemical Fire", "CRITICAL", "1000 sq meters", 7),
        "hospital": (4.6, "Hospital/Medical Fire", "CRITICAL", "800 sq meters", 6),
        "school": (4.0, "Educational Institution Fire", "HIGH", "600 sq meters", 4),
        "mall": (4.3, "Commercial Complex Fire", "HIGH", "3000 sq meters", 5),
        "forest": (3.8, "Forest/Wildfire", "HIGH", "5000 sq meters", 5),
        "building": (3.5, "Residential Building Fire", "HIGH", "400 sq meters", 3),
        "apartment": (3.3, "Apartment Fire", "MODERATE", "200 sq meters", 3),
        "kitchen": (2.0, "Kitchen/Domestic Fire", "LOW", "30 sq meters", 1),
        "electrical": (3.0, "Electrical Fire", "MODERATE", "100 sq meters", 2),
        "vehicle": (2.5, "Vehicle Fire", "MODERATE", "20 sq meters", 1),
        "gas": (4.0, "Gas Leak Fire", "HIGH", "300 sq meters", 4),
        "trapped": (4.5, fire_type, "CRITICAL", area, 5),
        "explosion": (5.0, "Explosion Fire", "CRITICAL", "3000 sq meters", 8),
        "spread": (3.8, fire_type, "HIGH", "500 sq meters", 4),
        "smoke": (2.8, fire_type, "MODERATE", "150 sq meters", 2),
    }

    for keyword, values in keyword_map.items():
        if keyword in desc_lower:
            score, fire_type, risk, area, units = values
            break

    # Category boost
    cat_map = {"industrial": 0.5, "building": 0.3, "forest": 0.4, "gas_leak": 0.6}
    score += cat_map.get(category, 0)
    score = min(5.0, max(1.0, score + random.uniform(-0.3, 0.3)))
    severity_int = max(1, min(5, round(score)))

    analysis_text = (
        f"🔥 **AI Fire Analysis Report**\n\n"
        f"**Fire Classification:** {fire_type}\n"
        f"**Severity Score:** {score:.1f}/5.0\n"
        f"**Risk Level:** {risk}\n\n"
        f"**Assessment:** Based on the incident report, this is classified as a {fire_type.lower()} "
        f"with {risk.lower()} risk level. The estimated affected area is approximately {area}. "
        f"Immediate deployment of {units} response unit(s) is recommended.\n\n"
        f"**Recommended Actions:**\n"
        f"- Deploy {units} fire response unit(s)\n"
        f"- {'Evacuate surrounding buildings immediately' if severity_int >= 4 else 'Establish safety perimeter'}\n"
        f"- {'Request mutual aid from neighboring stations' if severity_int >= 4 else 'Standard response protocol'}\n"
        f"- {'Alert hospitals for potential casualties' if severity_int >= 3 else 'Monitor situation'}\n"
        f"- Coordinate with local police for traffic and crowd control"
    )

    return AIAnalysis(
        severity_score=round(score, 1), fire_type=fire_type,
        risk_level=risk, estimated_affected_area=area,
        recommended_units=units, analysis_text=analysis_text,
        confidence_score=round(random.uniform(0.78, 0.95), 2))

def run_analysis_on_incident(incident_id: str) -> Optional[AIAnalysis]:
    inc = incidents_db.get(incident_id)
    if not inc:
        return None
    analysis = analyze_fire_severity(inc["description"], inc.get("category", "other"),
                                     inc["latitude"], inc["longitude"])
    inc["ai_analysis"] = analysis.model_dump()
    inc["severity"] = max(1, min(5, round(analysis.severity_score)))
    inc["updated_at"] = now_iso()
    return analysis

# ═══════════════════════════════════════════════════════════
# CHATBOT SERVICE
# ═══════════════════════════════════════════════════════════
CHAT_RESPONSES = {
    "en": {
        "evacuation": {
            "keywords": ["evacuate", "escape", "exit", "get out", "leave", "building fire"],
            "response": (
                "🚨 **Building Fire Evacuation Guide:**\n\n"
                "1. **Stay calm** and alert everyone nearby\n"
                "2. **Feel the door** before opening — if hot, DO NOT open\n"
                "3. **Stay low** — crawl below smoke level\n"
                "4. **Use stairs ONLY** — never use elevators\n"
                "5. **Cover nose and mouth** with a wet cloth\n"
                "6. **Go to the nearest exit** — follow EXIT signs\n"
                "7. **Close doors behind you** to slow fire spread\n"
                "8. **Meet at the assembly point** outside\n"
                "9. **Call 101** once you are safe\n\n"
                "⚠️ If trapped: Seal door gaps with wet cloth, signal from window"
            ),
            "suggestions": ["First aid for burns", "What if I'm trapped?", "Help for children", "Call 101"]
        },
        "burns": {
            "keywords": ["burn", "first aid", "treatment", "hurt", "skin", "scalded"],
            "response": (
                "🏥 **First Aid for Burns:**\n\n"
                "**Immediate Steps:**\n"
                "1. **Cool the burn** under running cold water for 10-20 minutes\n"
                "2. **Remove jewelry/clothing** near the burn (if not stuck)\n"
                "3. **Cover with clean cloth** or sterile bandage\n"
                "4. **Do NOT apply ice, butter, or toothpaste**\n"
                "5. **Do NOT pop blisters**\n\n"
                "**Seek emergency help (108) if:**\n"
                "- Burns cover large area (bigger than palm)\n"
                "- Burns on face, hands, feet, or joints\n"
                "- Chemical or electrical burns\n"
                "- Victim is a child or elderly person\n"
                "- Victim has difficulty breathing"
            ),
            "suggestions": ["Smoke inhalation help", "Chemical burn treatment", "When to call ambulance", "Evacuation guide"]
        },
        "smoke": {
            "keywords": ["smoke", "inhalation", "breathing", "cough", "fumes", "toxic"],
            "response": (
                "💨 **Smoke Inhalation Treatment:**\n\n"
                "1. **Move to fresh air immediately**\n"
                "2. **Call 108** (ambulance) right away\n"
                "3. **Sit upright** to help breathing\n"
                "4. **Loosen tight clothing** around neck and chest\n"
                "5. **If unconscious:** place in recovery position\n"
                "6. **If not breathing:** begin CPR if trained\n\n"
                "⚠️ Symptoms to watch: coughing, wheezing, headache, confusion, nausea\n\n"
                "Smoke inhalation can be life-threatening even without visible burns. Always seek medical attention."
            ),
            "suggestions": ["CPR instructions", "Recovery position", "Call ambulance", "First aid for burns"]
        },
        "electrical": {
            "keywords": ["electric", "wire", "short circuit", "current", "shock", "power"],
            "response": (
                "⚡ **Electrical Fire Safety:**\n\n"
                "**DO:**\n"
                "- Turn off the main power supply if safely accessible\n"
                "- Use a dry chemical (ABC) fire extinguisher\n"
                "- Call 101 immediately\n"
                "- Evacuate if the fire spreads\n\n"
                "**DO NOT:**\n"
                "- Use water on electrical fires\n"
                "- Touch the person if they're being electrocuted\n"
                "- Try to unplug burning appliances\n"
                "- Stand in water near electrical fires\n\n"
                "⚠️ Use a non-conducting object (wood, rubber) to separate victim from electrical source"
            ),
            "suggestions": ["How to use extinguisher", "Evacuation guide", "First aid for shock", "Call 101"]
        },
        "trapped": {
            "keywords": ["trapped", "stuck", "can't get out", "locked", "no exit", "surrounded"],
            "response": (
                "🆘 **If You Are Trapped in a Fire:**\n\n"
                "1. **Stay calm** — panic wastes energy and oxygen\n"
                "2. **Close all doors** between you and the fire\n"
                "3. **Seal gaps** under doors with wet towels or cloth\n"
                "4. **Move to a room with a window** if possible\n"
                "5. **Signal for help** — wave cloth from window, use phone flashlight\n"
                "6. **Call 101 and 112** — tell them your exact location and floor\n"
                "7. **Stay low** — air is cleaner near the floor\n"
                "8. **If you must move through smoke**, crawl on hands and knees\n"
                "9. **DO NOT jump** from high floors — wait for rescue\n\n"
                "🔴 Keep your phone charged and line open for rescue teams"
            ),
            "suggestions": ["Signal for help", "Smoke inhalation", "Call emergency", "Evacuation guide"]
        },
        "children": {
            "keywords": ["child", "children", "kid", "baby", "elderly", "old", "disabled", "senior"],
            "response": (
                "👶👴 **Evacuating Children, Elderly & Disabled:**\n\n"
                "**Children:**\n"
                "- Keep them close, hold their hand\n"
                "- Carry infants and toddlers\n"
                "- Cover their face with wet cloth\n"
                "- Reassure them — avoid panic\n"
                "- Never leave them alone\n\n"
                "**Elderly/Disabled:**\n"
                "- Assist with mobility, use wheelchair if available\n"
                "- Guide visually impaired persons by holding their arm\n"
                "- For hearing impaired — use gestures, write on phone\n"
                "- If mobility-limited: move to a safe room with window and call 101\n"
                "- Inform rescue teams of their location"
            ),
            "suggestions": ["Evacuation guide", "First aid for burns", "Call ambulance", "Pet evacuation"]
        },
        "extinguisher": {
            "keywords": ["extinguisher", "put out", "stop fire", "fight fire", "control fire"],
            "response": (
                "🧯 **How to Use a Fire Extinguisher (PASS Method):**\n\n"
                "**P** — **Pull** the pin\n"
                "**A** — **Aim** at the base of the fire\n"
                "**S** — **Squeeze** the handle\n"
                "**S** — **Sweep** side to side\n\n"
                "⚠️ **Important:**\n"
                "- Only fight small fires (smaller than a dustbin)\n"
                "- Keep your back to an exit\n"
                "- Maintain 2-3 meter distance\n"
                "- If fire doesn't reduce in 30 seconds — EVACUATE\n"
                "- Never use water extinguisher on oil/electrical fires"
            ),
            "suggestions": ["Types of extinguishers", "When to evacuate", "Electrical fire safety", "Call 101"]
        },
        "default": {
            "response": (
                "🔥 **FireShield AI Emergency Assistant**\n\n"
                "I can help you with fire emergencies. What do you need help with?\n\n"
                "• Building evacuation procedures\n"
                "• First aid for burns\n"
                "• Smoke inhalation treatment\n"
                "• Electrical fire safety\n"
                "• What to do if trapped\n"
                "• Evacuating children & elderly\n"
                "• Using fire extinguishers\n\n"
                "📞 **Emergency Numbers:**\n"
                "- 🚒 Fire: **101**\n"
                "- 🚑 Ambulance: **108**\n"
                "- 🚔 Police: **100**\n"
                "- 📱 Emergency: **112**"
            ),
            "suggestions": ["Evacuation guide", "First aid for burns", "I'm trapped", "Electrical fire safety"]
        }
    },
    "hi": {
        "evacuation": {
            "keywords": ["निकलना", "भागना", "बचाव", "बाहर", "आग लगी", "इमारत"],
            "response": (
                "🚨 **आग में बचाव गाइड:**\n\n"
                "1. **शांत रहें** और सभी को सतर्क करें\n"
                "2. **दरवाज़ा छूकर देखें** — गर्म हो तो न खोलें\n"
                "3. **नीचे रहें** — धुएं से बचने के लिए रेंगें\n"
                "4. **सीढ़ियों का उपयोग करें** — लिफ्ट कभी न लें\n"
                "5. **गीले कपड़े से नाक-मुंह ढकें**\n"
                "6. **निकटतम निकास की ओर जाएं**\n"
                "7. **सुरक्षित होने पर 101 पर कॉल करें**\n\n"
                "⚠️ फंसे हों तो: दरवाज़े की दरारें गीले कपड़े से बंद करें, खिड़की से संकेत दें"
            ),
            "suggestions": ["जलने पर प्राथमिक उपचार", "फंसे होने पर क्या करें", "101 पर कॉल करें", "बच्चों की सुरक्षा"]
        },
        "default": {
            "response": (
                "🔥 **फायरशील्ड AI आपातकालीन सहायक**\n\n"
                "मैं आग की आपात स्थिति में आपकी मदद कर सकता हूं:\n\n"
                "• इमारत से बचाव प्रक्रिया\n"
                "• जलने पर प्राथमिक उपचार\n"
                "• धुआं सांस में जाने पर उपचार\n"
                "• बिजली की आग से सुरक्षा\n"
                "• फंसे होने पर क्या करें\n\n"
                "📞 **आपातकालीन नंबर:**\n"
                "- 🚒 दमकल: **101**\n"
                "- 🚑 एम्बुलेंस: **108**\n"
                "- 🚔 पुलिस: **100**\n"
                "- 📱 इमरजेंसी: **112**"
            ),
            "suggestions": ["बचाव गाइड", "प्राथमिक उपचार", "मैं फंसा हूं", "101 पर कॉल करें"]
        }
    }
}

def get_chat_response(message: str, lang: str = "en") -> ChatResponse:
    msg_lower = message.lower()
    lang_data = CHAT_RESPONSES.get(lang, CHAT_RESPONSES["en"])

    for key, data in lang_data.items():
        if key == "default":
            continue
        keywords = data.get("keywords", [])
        if any(kw in msg_lower for kw in keywords):
            return ChatResponse(response=data["response"],
                                suggestions=data["suggestions"],
                                emergency_type=key)

    default = lang_data["default"]
    return ChatResponse(response=default["response"],
                        suggestions=default["suggestions"],
                        emergency_type="general")

# ═══════════════════════════════════════════════════════════
# LOCATION SERVICE
# ═══════════════════════════════════════════════════════════
FIRE_STATIONS = [
    {"id": "fs-001", "name": "Delhi Fire Service HQ", "latitude": 28.6328, "longitude": 77.2197, "address": "Connaught Place, New Delhi", "phone": "+91-11-23414000", "available_units": 6},
    {"id": "fs-002", "name": "Mumbai Central Fire Station", "latitude": 18.9690, "longitude": 72.8311, "address": "Byculla, Mumbai", "phone": "+91-22-23076111", "available_units": 5},
    {"id": "fs-003", "name": "Bangalore City Fire Station", "latitude": 12.9784, "longitude": 77.5719, "address": "Corporation Circle, Bangalore", "phone": "+91-80-22212121", "available_units": 4},
    {"id": "fs-004", "name": "Chennai Central Fire Station", "latitude": 13.0827, "longitude": 80.2707, "address": "Anna Salai, Chennai", "phone": "+91-44-25384000", "available_units": 5},
    {"id": "fs-005", "name": "Kolkata Fire Brigade HQ", "latitude": 22.5726, "longitude": 88.3639, "address": "Central Avenue, Kolkata", "phone": "+91-33-22861011", "available_units": 4},
    {"id": "fs-006", "name": "Hyderabad Fire Station", "latitude": 17.3850, "longitude": 78.4867, "address": "Abids, Hyderabad", "phone": "+91-40-24733333", "available_units": 5},
    {"id": "fs-007", "name": "Pune Fire Brigade", "latitude": 18.5204, "longitude": 73.8567, "address": "Shivajinagar, Pune", "phone": "+91-20-25501294", "available_units": 4},
    {"id": "fs-008", "name": "Jaipur Fire Station", "latitude": 26.9124, "longitude": 75.7873, "address": "MI Road, Jaipur", "phone": "+91-141-2565555", "available_units": 3},
    {"id": "fs-009", "name": "Ahmedabad Fire Station", "latitude": 23.0225, "longitude": 72.5714, "address": "Lal Darwaja, Ahmedabad", "phone": "+91-79-25391500", "available_units": 4},
    {"id": "fs-010", "name": "Lucknow Fire Service", "latitude": 26.8467, "longitude": 80.9462, "address": "Hazratganj, Lucknow", "phone": "+91-522-2612244", "available_units": 3},
]

HOSPITALS = [
    {"id": "h-001", "name": "AIIMS Delhi", "latitude": 28.5672, "longitude": 77.2100, "address": "Ansari Nagar, New Delhi", "phone": "+91-11-26588500", "has_burn_unit": True},
    {"id": "h-002", "name": "Safdarjung Hospital", "latitude": 28.5684, "longitude": 77.2068, "address": "Ring Road, New Delhi", "phone": "+91-11-26707437", "has_burn_unit": True},
    {"id": "h-003", "name": "KEM Hospital Mumbai", "latitude": 19.0003, "longitude": 72.8417, "address": "Parel, Mumbai", "phone": "+91-22-24107000", "has_burn_unit": True},
    {"id": "h-004", "name": "Victoria Hospital Bangalore", "latitude": 12.9585, "longitude": 77.5730, "address": "Fort Road, Bangalore", "phone": "+91-80-26701150", "has_burn_unit": True},
    {"id": "h-005", "name": "Apollo Hospital Chennai", "latitude": 13.0067, "longitude": 80.2206, "address": "Greams Road, Chennai", "phone": "+91-44-28290200", "has_burn_unit": True},
    {"id": "h-006", "name": "SSKM Hospital Kolkata", "latitude": 22.5361, "longitude": 88.3441, "address": "AJC Bose Road, Kolkata", "phone": "+91-33-22041101", "has_burn_unit": True},
    {"id": "h-007", "name": "Osmania Hospital Hyderabad", "latitude": 17.3753, "longitude": 78.4744, "address": "Afzalgunj, Hyderabad", "phone": "+91-40-24600146", "has_burn_unit": True},
    {"id": "h-008", "name": "Sassoon Hospital Pune", "latitude": 18.5308, "longitude": 73.8745, "address": "Sassoon Road, Pune", "phone": "+91-20-26128000", "has_burn_unit": True},
]

POLICE_STATIONS = [
    {"id": "p-001", "name": "Parliament Street PS", "latitude": 28.6215, "longitude": 77.2145, "address": "Parliament Street, New Delhi", "phone": "+91-11-23361600"},
    {"id": "p-002", "name": "Colaba Police Station", "latitude": 18.9067, "longitude": 72.8147, "address": "Colaba, Mumbai", "phone": "+91-22-22841717"},
    {"id": "p-003", "name": "Cubbon Park PS", "latitude": 12.9763, "longitude": 77.5929, "address": "Cubbon Park, Bangalore", "phone": "+91-80-22942342"},
    {"id": "p-004", "name": "Egmore Police Station", "latitude": 13.0732, "longitude": 80.2609, "address": "Egmore, Chennai", "phone": "+91-44-28190000"},
    {"id": "p-005", "name": "Lal Bazar PS", "latitude": 22.5697, "longitude": 88.3495, "address": "Lal Bazar, Kolkata", "phone": "+91-33-22503028"},
]

def find_nearby(lat: float, lng: float, service_type: str, radius_km: float = 15.0) -> List[NearbyService]:
    if service_type == "fire_station":
        source = FIRE_STATIONS
    elif service_type == "hospital":
        source = HOSPITALS
    elif service_type == "police":
        source = POLICE_STATIONS
    else:
        return []

    results = []
    for s in source:
        dist = haversine_distance(lat, lng, s["latitude"], s["longitude"])
        if dist <= radius_km:
            results.append(NearbyService(
                id=s["id"], name=s["name"],
                latitude=s["latitude"], longitude=s["longitude"],
                address=s["address"], phone=s["phone"],
                distance_km=dist, service_type=service_type,
                available_units=s.get("available_units"),
                has_burn_unit=s.get("has_burn_unit")))
    results.sort(key=lambda x: x.distance_km)
    return results[:5]

# ═══════════════════════════════════════════════════════════
# NOTIFICATION SERVICE
# ═══════════════════════════════════════════════════════════
def send_sos_notification(incident_id: str, lat: float, lng: float):
    stations = find_nearby(lat, lng, "fire_station", 20)
    for station in stations[:3]:
        notifications_log.append({
            "id": generate_uuid(), "type": "sos_alert",
            "title": f"🚨 SOS: Fire Emergency",
            "body": f"Incident {incident_id} reported near {station.name}",
            "recipient": station.name, "incident_id": incident_id,
            "timestamp": now_iso()})
    return len(stations[:3])

# ═══════════════════════════════════════════════════════════
# ANALYTICS SERVICE
# ═══════════════════════════════════════════════════════════
def get_dashboard_summary() -> DashboardSummary:
    all_inc = list(incidents_db.values())
    total = len(all_inc)
    active = len([i for i in all_inc if i["status"] not in ("resolved",)])
    resolved_today = len([i for i in all_inc if i["status"] == "resolved"])

    response_times = [i["response_time_mins"] for i in all_inc if i.get("response_time_mins")]
    avg_rt = round(sum(response_times) / len(response_times), 1) if response_times else 0

    by_severity = {}
    for i in all_inc:
        s = str(i["severity"])
        by_severity[s] = by_severity.get(s, 0) + 1

    by_status = {}
    for i in all_inc:
        by_status[i["status"]] = by_status.get(i["status"], 0) + 1

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    trend = [{"month": m, "count": random.randint(15, 45)} for m in months]

    return DashboardSummary(
        total_incidents=total, active_incidents=active,
        resolved_today=resolved_today, avg_response_time_mins=avg_rt,
        incidents_by_severity=by_severity, incidents_by_status=by_status,
        monthly_trend=trend)

def get_heatmap_data() -> List[HeatmapPoint]:
    return [HeatmapPoint(latitude=i["latitude"], longitude=i["longitude"],
                         intensity=min(1.0, i["severity"] / 5.0))
            for i in incidents_db.values()]

def get_timeline() -> List[TimelineEvent]:
    events = []
    for inc in sorted(incidents_db.values(), key=lambda x: x["created_at"], reverse=True)[:20]:
        events.append(TimelineEvent(
            id=inc["id"], type="incident",
            title=f"{'🔴' if inc['severity']>=4 else '🟡' if inc['severity']>=3 else '🟢'} {inc['title']}",
            description=inc["address"],
            severity=inc["severity"], timestamp=inc["created_at"]))
    return events

# ═══════════════════════════════════════════════════════════
# SEED DATA
# ═══════════════════════════════════════════════════════════
def seed_demo_data():
    """Pre-populate with demo users and realistic Indian fire incidents."""
    # Demo users
    demo_users = [
        {"id": "demo-citizen-001", "name": "Rahul Sharma", "email": "citizen@demo.com", "phone": "+91-9876543210", "role": "citizen"},
        {"id": "demo-official-001", "name": "Inspector Priya Singh", "email": "official@demo.com", "phone": "+91-9876543211", "role": "official"},
        {"id": "demo-admin-001", "name": "Chief Controller", "email": "admin@demo.com", "phone": "+91-9876543212", "role": "admin"},
    ]
    for u in demo_users:
        users_db[u["id"]] = {**u, "avatar_url": None, "created_at": "2025-01-01T00:00:00Z",
                             "password_hash": pwd_context.hash("demo123")}

    # Realistic sample incidents
    sample_incidents = [
        {"title": "Factory Fire at Manesar Industrial Area", "desc": "Major industrial fire in factory unit. Chemical storage nearby. Workers trapped on second floor.", "lat": 28.3590, "lon": 76.9366, "addr": "IMT Manesar, Gurgaon, Haryana", "cat": "industrial", "sev": 5, "status": "en_route", "team": "Alpha Team", "rt": 6.5},
        {"title": "Residential Building Fire in Lajpat Nagar", "desc": "Fire broke out on 4th floor of apartment building. Smoke spreading to upper floors.", "lat": 28.5700, "lon": 77.2370, "addr": "Block C, Lajpat Nagar II, New Delhi", "cat": "building", "sev": 4, "status": "assigned", "team": "Bravo Team", "rt": 8.2},
        {"title": "Kitchen Fire in Andheri Restaurant", "desc": "Kitchen grease fire in restaurant during peak hours. Staff evacuated customers.", "lat": 19.1136, "lon": 72.8697, "addr": "Andheri West, Mumbai, Maharashtra", "cat": "kitchen", "sev": 2, "status": "resolved", "team": "Charlie Team", "rt": 5.0},
        {"title": "Electrical Fire at Koramangala Office", "desc": "Short circuit fire in server room of IT office building. Sprinklers activated.", "lat": 12.9352, "lon": 77.6245, "addr": "5th Block, Koramangala, Bangalore", "cat": "electrical", "sev": 3, "status": "resolved", "team": "Delta Team", "rt": 7.3},
        {"title": "Warehouse Fire in Ambattur Industrial Estate", "desc": "Large warehouse storing textiles caught fire. Fire spread rapidly due to flammable materials.", "lat": 13.1143, "lon": 80.1548, "addr": "Ambattur Industrial Estate, Chennai", "cat": "industrial", "sev": 5, "status": "arrived", "team": "Alpha Team", "rt": 9.1},
        {"title": "Forest Fire in Bandipur National Park", "desc": "Forest fire spotted in the eastern section. Dry conditions causing rapid spread.", "lat": 11.6700, "lon": 76.6300, "addr": "Bandipur National Park, Karnataka", "cat": "forest", "sev": 4, "status": "en_route", "team": "Forest Response Unit", "rt": 15.0},
        {"title": "Gas Leak Fire at Chandni Chowk Market", "desc": "LPG gas cylinder explosion in market area. Multiple shops affected.", "lat": 28.6506, "lon": 77.2302, "addr": "Chandni Chowk, Old Delhi", "cat": "gas_leak", "sev": 4, "status": "arrived", "team": "Bravo Team", "rt": 5.5},
        {"title": "Vehicle Fire on NH-48 Expressway", "desc": "Truck carrying chemicals caught fire on the expressway near Huda City Centre.", "lat": 28.4595, "lon": 77.0266, "addr": "NH-48, Near Huda City Centre, Gurgaon", "cat": "vehicle", "sev": 3, "status": "resolved", "team": "Highway Rescue", "rt": 12.0},
        {"title": "Shopping Mall Fire in Salt Lake City", "desc": "Fire alarm triggered at 3rd floor of shopping mall. Smoke detected in food court.", "lat": 22.5806, "lon": 88.4137, "addr": "City Centre, Salt Lake, Kolkata", "cat": "building", "sev": 3, "status": "acknowledged", "team": None, "rt": None},
        {"title": "Hospital Generator Fire in Jubilee Hills", "desc": "Generator room fire in hospital basement. Backup power disrupted. Patients stable.", "lat": 17.4325, "lon": 78.4073, "addr": "Jubilee Hills, Hyderabad, Telangana", "cat": "electrical", "sev": 4, "status": "assigned", "team": "Echo Team", "rt": 4.2},
        {"title": "Slum Fire in Dharavi", "desc": "Fire spread across multiple shanties in Dharavi. Dense area making access difficult.", "lat": 19.0434, "lon": 72.8550, "addr": "Dharavi, Mumbai, Maharashtra", "cat": "building", "sev": 5, "status": "arrived", "team": "Alpha Team", "rt": 7.8},
        {"title": "College Lab Fire in IIT Delhi", "desc": "Chemical lab fire in Chemistry department. Students evacuated safely.", "lat": 28.5450, "lon": 77.1926, "addr": "IIT Delhi, Hauz Khas, New Delhi", "cat": "electrical", "sev": 3, "status": "resolved", "team": "Campus Response", "rt": 3.5},
        {"title": "Godown Fire in MIDC Pune", "desc": "Plastic raw material godown caught fire. Toxic fumes reported. Area being evacuated.", "lat": 18.5904, "lon": 73.7395, "addr": "MIDC Bhosari, Pune, Maharashtra", "cat": "industrial", "sev": 4, "status": "en_route", "team": "Charlie Team", "rt": 10.5},
        {"title": "Temple Fire during Festival", "desc": "Decorative fire spread at temple during festival. Panic among devotees.", "lat": 26.9124, "lon": 75.7873, "addr": "Govind Dev Ji Temple, Jaipur, Rajasthan", "cat": "other", "sev": 3, "status": "resolved", "team": "Jaipur Fire", "rt": 6.0},
        {"title": "Hostel Kitchen Fire at JNU", "desc": "Minor kitchen fire in university hostel mess. Extinguished by staff.", "lat": 28.5402, "lon": 77.1674, "addr": "JNU Campus, New Delhi", "cat": "kitchen", "sev": 1, "status": "resolved", "team": None, "rt": 2.0},
        {"title": "Construction Site Fire in Noida", "desc": "Fire at under-construction high-rise. Building materials caught fire. No workers present.", "lat": 28.5355, "lon": 77.3910, "addr": "Sector 150, Noida, Uttar Pradesh", "cat": "building", "sev": 2, "status": "resolved", "team": "Noida Fire", "rt": 8.0},
        {"title": "Bus Depot Fire in Nehru Place", "desc": "DTC bus caught fire at depot. Fuel tank risk. Adjacent buses being moved.", "lat": 28.5491, "lon": 77.2538, "addr": "Nehru Place Bus Depot, New Delhi", "cat": "vehicle", "sev": 3, "status": "assigned", "team": "Bravo Team", "rt": 5.8},
        {"title": "Firecracker Warehouse Fire", "desc": "Illegal firecracker storage caught fire. Multiple explosions heard. Area cordoned off.", "lat": 13.0827, "lon": 80.2707, "addr": "Sivakasi Warehouse, Chennai", "cat": "industrial", "sev": 5, "status": "en_route", "team": "Delta Team", "rt": 11.0},
    ]

    base_time = datetime.utcnow() - timedelta(days=30)
    for i, s in enumerate(sample_incidents):
        ts = (base_time + timedelta(days=i * 1.5, hours=random.randint(0, 23))).isoformat() + "Z"
        iid = f"INC-{1001 + i}"
        history = [{"status": "reported", "timestamp": ts, "updated_by": "system"}]
        if s["status"] != "reported":
            history.append({"status": s["status"], "timestamp": ts, "updated_by": "dispatcher"})

        analysis = analyze_fire_severity(s["desc"], s["cat"], s["lat"], s["lon"])

        incidents_db[iid] = {
            "id": iid, "user_id": "demo-citizen-001", "user_name": "Rahul Sharma",
            "title": s["title"], "description": s["desc"],
            "latitude": s["lat"], "longitude": s["lon"],
            "address": s["addr"], "category": s["cat"],
            "severity": s["sev"], "status": s["status"],
            "media_urls": [], "ai_analysis": analysis.model_dump(),
            "assigned_team": s["team"], "created_at": ts, "updated_at": ts,
            "response_time_mins": s["rt"], "status_history": history,
        }
