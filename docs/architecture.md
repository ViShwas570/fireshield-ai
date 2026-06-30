# FireShield AI — System Architecture

## High-Level Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        MA[📱 Flutter Mobile App]
        WD[🖥️ Web Dashboard]
    end

    subgraph "API Gateway"
        FA[⚙️ FastAPI Server]
        WS[🔌 WebSocket Server]
    end

    subgraph "Service Layer"
        AS[🔐 Auth Service]
        IS[📋 Incident Service]
        AI[🤖 AI Service]
        CB[💬 Chatbot Service]
        LS[📍 Location Service]
        NS[🔔 Notification Service]
        AN[📊 Analytics Service]
    end

    subgraph "Data Layer"
        FS[(🔥 Firestore)]
        FB[(📦 Firebase Storage)]
        FC[☁️ Firebase Cloud Messaging]
    end

    subgraph "External Services"
        GM[🗺️ Google Maps API]
        GE[🤖 Gemini AI API]
        ND[🏛️ NDMA API Simulated]
    end

    MA --> FA
    MA --> WS
    WD --> FA
    WD --> WS
    
    FA --> AS
    FA --> IS
    FA --> AI
    FA --> CB
    FA --> LS
    FA --> NS
    FA --> AN

    AS --> FS
    IS --> FS
    IS --> FB
    NS --> FC
    
    AI --> GE
    LS --> GM
    IS --> ND
```

## Component Details

### 1. Flutter Mobile App

```mermaid
graph LR
    subgraph "Presentation Layer"
        S[Screens]
        W[Widgets]
    end
    
    subgraph "State Layer"
        P[Riverpod Providers]
        N[StateNotifiers]
    end
    
    subgraph "Domain Layer"
        M[Models]
        R[Repositories]
    end
    
    subgraph "Data Layer"
        API[API Service]
        LOC[Location Service]
        STR[Storage Service]
    end

    S --> P
    W --> P
    P --> N
    N --> R
    R --> API
    R --> LOC
    R --> STR
    R --> M
```

**Features by Module:**

| Module | Screens | Key Functionality |
|--------|---------|-------------------|
| Auth | Splash, Onboarding, Login, Register | JWT auth, demo login |
| Home | Home Dashboard | SOS button, quick actions, emergency numbers |
| SOS | SOS Report | GPS capture, media upload, AI analysis |
| Chatbot | Chat Interface | Emergency guidance, multi-language |
| Map | Nearby Services | Google Maps integration, service locator |
| Incidents | List, Detail | History, timeline, status tracking |
| Profile | User Profile | Stats, emergency contacts |
| Settings | App Settings | Theme, language, notifications |

### 2. FastAPI Backend

```mermaid
graph TB
    subgraph "Routes Layer"
        AR[Auth Routes]
        IR[Incident Routes]
        LR[Location Routes]
        CR[Chat Routes]
        ANR[Analytics Routes]
        ER[Emergency Routes]
        WSR[WebSocket Routes]
    end

    subgraph "Service Layer"
        AUS[Auth Service]
        INS[Incident Service]
        AIS[AI Service]
        CBS[Chatbot Service]
        LOS[Location Service]
        NOS[Notification Service]
        ANS[Analytics Service]
    end

    subgraph "Data Layer"
        UDB[(Users Store)]
        IDB[(Incidents Store)]
        SDB[(Services Store)]
        NDB[(Notifications Log)]
    end

    AR --> AUS --> UDB
    IR --> INS --> IDB
    IR --> AIS
    LR --> LOS --> SDB
    CR --> CBS
    ANR --> ANS --> IDB
    ER --> INS
    ER --> NOS --> NDB
    WSR --> INS
```

### 3. Web Dashboard

```mermaid
graph TB
    subgraph "Views"
        DV[Dashboard View]
        MV[Map View]
        IV[Incidents View]
        AV[Analytics View]
        TV[Teams View]
    end

    subgraph "Services"
        API[API Service]
        WSS[WebSocket Client]
        DS[Data Service - Fallback]
    end

    subgraph "Libraries"
        CJ[Chart.js]
        LJ[Leaflet.js]
        FA[Font Awesome]
    end

    DV --> API
    DV --> CJ
    MV --> API
    MV --> LJ
    IV --> API
    AV --> API
    AV --> CJ
    TV --> API
    
    API --> WSS
    API --> DS
```

## Data Flow Diagrams

### SOS Emergency Flow

```mermaid
sequenceDiagram
    participant C as 👤 Citizen
    participant A as 📱 Mobile App
    participant B as ⚙️ Backend
    participant AI as 🤖 AI Service
    participant D as 🖥️ Dashboard
    participant F as 🚒 Fire Station

    C->>A: Tap SOS Button
    A->>A: Capture GPS, Time, User Info
    A->>A: Open SOS Form
    C->>A: Add Description + Media
    A->>B: POST /api/emergency/sos
    B->>AI: Analyze Severity
    AI-->>B: Severity Score + Analysis
    B->>B: Create Incident
    B->>D: WebSocket: New Incident
    B->>F: Notify Nearest Station
    B-->>A: Incident Created + Analysis
    A->>C: Show Confirmation + AI Report
    D->>D: Show Alert + Map Marker
    
    Note over D: Dispatcher Reviews
    D->>B: PUT /api/incidents/{id}/status
    B->>A: WebSocket: Status Update
    A->>C: Push Notification
```

### Chatbot Flow

```mermaid
sequenceDiagram
    participant U as 👤 User
    participant A as 📱 App
    participant B as ⚙️ Backend

    U->>A: Opens Chatbot
    A->>A: Show Welcome + Quick Options
    U->>A: "How to evacuate building fire?"
    A->>B: POST /api/chatbot/message
    B->>B: Match intent + Generate response
    B-->>A: Response + Suggestions
    A->>U: Display response + Quick reply chips
    U->>A: Taps "First aid for burns"
    A->>B: POST /api/chatbot/message
    B-->>A: Detailed first-aid instructions
    A->>U: Display with step-by-step guide
```

## Security Architecture

```mermaid
graph LR
    subgraph "Authentication"
        LOGIN[Login Request] --> JWT[JWT Token Generation]
        JWT --> TOKEN[Access Token]
    end

    subgraph "Authorization"
        TOKEN --> MW[Auth Middleware]
        MW --> ROLE{Role Check}
        ROLE -->|Citizen| CA[Citizen Access]
        ROLE -->|Official| OA[Official Access]
        ROLE -->|Admin| AA[Admin Access]
    end

    subgraph "API Security"
        CORS[CORS Policy]
        RATE[Rate Limiting]
        VAL[Input Validation]
    end
```

## Deployment Architecture (Production)

```mermaid
graph TB
    subgraph "CDN / Static"
        CF[CloudFlare CDN]
        FH[Firebase Hosting]
    end

    subgraph "Compute"
        CR[Cloud Run / GCE]
        CF2[Cloud Functions]
    end

    subgraph "Database"
        FS[(Firestore)]
        FB[(Firebase Storage)]
    end

    subgraph "Services"
        FCM[Firebase Cloud Messaging]
        GM[Google Maps Platform]
        GAI[Gemini AI API]
    end

    CF --> FH
    FH --> |Dashboard| CR
    CR --> |API| FS
    CR --> |Media| FB
    CR --> GAI
    CF2 --> FCM
    CR --> GM
```

## Scalability Considerations

| Aspect | Strategy |
|--------|----------|
| **Horizontal Scaling** | Stateless API design, can deploy multiple instances behind load balancer |
| **Database** | Firestore auto-scales, composite indexes for complex queries |
| **Media Storage** | Firebase Storage with CDN for fast media delivery |
| **Real-time** | WebSocket with connection pooling, fallback to polling |
| **Caching** | Redis layer for frequently accessed data (fire stations, analytics) |
| **AI Processing** | Async queue for AI analysis, batch processing for non-urgent analysis |
| **Geospatial** | GeoHash indexing for efficient proximity queries |
| **Monitoring** | Cloud Monitoring, error tracking, performance metrics |

## Technology Decision Rationale

| Decision | Rationale |
|----------|-----------|
| Flutter over React Native | Better performance, single codebase, Material 3 native support |
| FastAPI over Django/Express | Async support, auto-generated docs, Python ML ecosystem |
| Riverpod over BLoC | Less boilerplate, better testability, compile-time safety |
| Leaflet over Google Maps (Dashboard) | Free, no API key, OSM tiles, better for web dashboards |
| In-memory over Firebase (MVP) | Zero setup for hackathon demo, easy to swap for production |
| JWT over Session | Stateless, mobile-friendly, scalable |
| WebSocket over SSE | Bidirectional, lower latency, better for real-time dispatch |
