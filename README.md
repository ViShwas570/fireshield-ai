🔥 FireShield AI
AI-Powered Emergency Response Ecosystem for India
<p align="center">
  <img src="docs/logo.svg" alt="FireShield AI Logo" width="120"/>
</p>
<p align="center">
  <strong>🏆 National Hackathon Project — "The Last-Minute Life Saver"</strong>
</p>
<p align="center">
  <a href="#features">Features</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#tech-stack">Tech Stack</a> •
  <a href="#setup">Setup</a> •
  <a href="#demo">Demo</a> •
  <a href="#api">API Docs</a>
</p>
---
🌐 Live Demo
Component	Link
🖥️ Dashboard	fireshield-ai.vercel.app
⚙️ Backend API Docs	fireshield-ai-p41f.onrender.com/docs
> Note: the backend is hosted on Render's free tier, which sleeps after inactivity — the first request may take ~20-30 seconds to wake up.
---
📋 Problem Statement
India faces a growing crisis of fire accidents across homes, hostels, schools, colleges, hospitals, factories, shopping malls, forests, and commercial buildings. The lack of a unified, intelligent emergency response system results in delayed responses, poor coordination, and preventable casualties.
💡 Our Solution
FireShield AI is not just a fire reporting app — it's a complete AI-powered emergency response ecosystem that connects citizens with fire departments through intelligent automation, real-time tracking, and AI-driven decision support.
Three Integrated Components:
Component	Target Users	Technology
📱 Mobile App	Citizens	Flutter + Material 3
🖥️ Command Dashboard	Fire Officials	HTML/CSS/JS + Leaflet
⚙️ Backend API	System Core	FastAPI + Python
---
✨ Features {#features}
📱 Citizen Mobile App
Feature	Description
🆘 One-Tap SOS	Emergency button that captures GPS, time, user details, and media in one tap
🤖 AI Severity Analysis	Gemini AI analyzes reported incidents for fire type, severity, and recommended response
💬 Emergency Chatbot	AI-powered chatbot providing evacuation guidance and first-aid instructions
🗺️ Nearby Services	Locate nearest fire stations, hospitals, and police stations with directions
📸 Media Upload	Capture and upload photos/videos of the incident for AI analysis
📍 Live Location	Real-time location sharing with emergency contacts and responders
🔔 Push Notifications	Real-time updates on incident status and emergency alerts
🌐 Multilingual	Full support for English and Hindi
📴 Offline Mode	Cache critical data for use without internet connectivity
🎨 Premium UI	Material 3 with glassmorphism, animations, dark/light mode
📊 Incident History	Track all reported incidents with status timeline
📞 Emergency Numbers	Quick-dial 101, 112, 108, 100 directly from the app
🖥️ Fire Department Dashboard
Feature	Description
🗺️ Live Incident Map	Interactive map showing all incidents with severity-coded markers
📊 Real-Time Analytics	Response time metrics, severity distribution, trend analysis
🚒 Dispatcher Controls	Assign teams, update status, manage response workflow
🔥 Heatmap	Identify fire-prone areas with geographic heatmap overlays
📋 Incident Management	Full CRUD with filtering, sorting, search, and bulk operations
🤖 AI Insights	View AI-generated severity analysis for each incident
👥 Team Management	Track team status, assignments, and performance
⏱️ Timeline View	Chronological incident status changes with timestamps
📈 Performance Metrics	Average response time, resolution rate, team efficiency
🔄 Real-Time Updates	WebSocket-powered live data feeds
⚙️ Backend API
Feature	Description
🔐 JWT Authentication	Secure token-based authentication with role management
📡 RESTful API	Comprehensive endpoints for all operations
🔌 WebSocket	Real-time bidirectional communication
🤖 AI Integration	Simulated Gemini API for fire severity analysis
💬 Chatbot Engine	Rule-based emergency guidance in English and Hindi
📍 Location Services	Nearby services with haversine distance calculation
📊 Analytics Engine	Aggregated metrics and trend computation
🔔 Notification System	Simulated push notification infrastructure
---
🏗️ Architecture {#architecture}
```
┌─────────────────────────────────────────────────────────────┐
│                    FireShield AI Ecosystem                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    REST API    ┌──────────────────────┐   │
│  │  📱 Flutter   │──────────────▶│   ⚙️ FastAPI Backend  │   │
│  │  Mobile App   │◀──────────────│                      │   │
│  │              │               │  ┌────────────────┐  │   │
│  │  • SOS       │               │  │ 🤖 AI Service   │  │   │
│  │  • Chatbot   │    WebSocket  │  │ (Gemini Sim)   │  │   │
│  │  • Maps      │◀─────────────▶│  ├────────────────┤  │   │
│  │  • Profile   │               │  │ 💬 Chatbot Svc  │  │   │
│  └──────────────┘               │  ├────────────────┤  │   │
│                                  │  │ 📍 Location Svc │  │   │
│  ┌──────────────┐    REST API   │  ├────────────────┤  │   │
│  │  🖥️ Web       │──────────────▶│  │ 📊 Analytics    │  │   │
│  │  Dashboard   │◀──────────────│  ├────────────────┤  │   │
│  │              │               │  │ 🔔 Notification │  │   │
│  │  • Live Map  │    WebSocket  │  └────────────────┘  │   │
│  │  • Analytics │◀─────────────▶│                      │   │
│  │  • Dispatch  │               │  ┌────────────────┐  │   │
│  │  • Teams     │               │  │ 💾 In-Memory DB │  │   │
│  └──────────────┘               │  │ (Simulated)    │  │   │
│                                  │  └────────────────┘  │   │
│                                  └──────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```
Data Flow
```
Citizen Reports Fire
        │
        ▼
  ┌─────────────┐
  │ GPS + Media  │
  │ + Details    │
  └──────┬──────┘
         │
         ▼
  ┌─────────────┐     ┌──────────────┐
  │  FastAPI     │────▶│  AI Analysis  │
  │  Backend     │◀────│  (Gemini Sim) │
  └──────┬──────┘     └──────────────┘
         │
    ┌────┴─────┐
    ▼          ▼
┌────────┐ ┌────────────┐
│Dashboard│ │Notification│
│  Alert  │ │ to Nearby  │
│         │ │ Stations   │
└────────┘ └────────────┘
    │
    ▼
┌─────────────┐
│ Dispatcher   │
│ Assigns Team │
│ Tracks Status│
└─────────────┘
```
---
🛠️ Tech Stack {#tech-stack}
Layer	Technology	Purpose
Mobile	Flutter 3.x	Cross-platform mobile app
State Management	Riverpod	Reactive state management
Navigation	GoRouter	Declarative routing
HTTP Client	Dio	API communication
UI Framework	Material 3	Premium design system
Backend	FastAPI	High-performance Python API
Authentication	JWT (python-jose)	Secure token auth
AI	Gemini API (Simulated)	Fire severity analysis
Dashboard	HTML/CSS/JS	Responsive web dashboard
Maps (Dashboard)	Leaflet.js + OSM	Free, no API key needed
Maps (Mobile)	Google Maps Flutter	Native mobile maps
Charts	Chart.js	Analytics visualization
Real-time	WebSocket	Live data updates
---
🚀 Setup & Installation {#setup}
Prerequisites
Python 3.9+ with pip
Flutter 3.x SDK
Android Studio / VS Code
A modern web browser (Chrome/Firefox/Edge)
1️⃣ Backend Setup
```bash
# Navigate to backend directory
cd fireshield-ai/backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run the server
python run.py
```
The API will be available at http://localhost:8000
📝 API documentation: http://localhost:8000/docs (Swagger UI)
2️⃣ Dashboard Setup
```bash
# Simply open the dashboard in a browser
# Option 1: Direct file
open fireshield-ai/dashboard/index.html

# Option 2: Using Python HTTP server (recommended)
cd fireshield-ai/dashboard
python -m http.server 3000

# Then open http://localhost:3000
```
> **Note:** The dashboard works completely standalone with sample data. Start the backend API for live data.
3️⃣ Mobile App Setup
```bash
# Navigate to mobile directory
cd fireshield-ai/mobile

# Get dependencies
flutter pub get

# Run on connected device/emulator
flutter run

# Build APK
flutter build apk --release
```
Google Maps API Key (Optional)
For map functionality in the mobile app, add your Google Maps API key:
Android: `mobile/android/app/src/main/AndroidManifest.xml`
```xml
<meta-data
    android:name="com.google.android.geo.API_KEY"
    android:value="YOUR_API_KEY"/>
```
iOS: `mobile/ios/Runner/AppDelegate.swift`
```swift
GMSServices.provideAPIKey("YOUR_API_KEY")
```
> The app includes a fallback list view when Google Maps is not configured.
---
🔑 Demo Credentials {#demo}
Role	Email	Password
👤 Citizen	citizen@demo.com	demo123
🧑‍🚒 Official	official@demo.com	demo123
👨‍💼 Admin	admin@demo.com	demo123
---
📡 API Documentation {#api}
Authentication
Method	Endpoint	Description
`POST`	`/api/auth/register`	Register new user
`POST`	`/api/auth/login`	Login & get JWT token
`GET`	`/api/auth/profile`	Get current user profile
Incidents
Method	Endpoint	Description
`POST`	`/api/incidents`	Report new incident
`GET`	`/api/incidents`	List all incidents (filterable)
`GET`	`/api/incidents/{id}`	Get incident details
`PUT`	`/api/incidents/{id}/status`	Update incident status
`POST`	`/api/incidents/{id}/analyze`	Run AI severity analysis
Emergency
Method	Endpoint	Description
`POST`	`/api/emergency/sos`	Trigger SOS emergency
Nearby Services
Method	Endpoint	Description
`GET`	`/api/nearby/fire-stations`	Find nearby fire stations
`GET`	`/api/nearby/hospitals`	Find nearby hospitals
`GET`	`/api/nearby/police`	Find nearby police stations
Chatbot
Method	Endpoint	Description
`POST`	`/api/chatbot/message`	Send message to emergency chatbot
Analytics
Method	Endpoint	Description
`GET`	`/api/analytics/summary`	Dashboard summary metrics
`GET`	`/api/analytics/heatmap`	Heatmap data points
`GET`	`/api/analytics/timeline`	Recent event timeline
WebSocket
Protocol	Endpoint	Description
`WS`	`/ws/incidents`	Real-time incident updates
> Full interactive API docs available at **https://fireshield-ai-p41f.onrender.com/docs** (live) or **http://localhost:8000/docs** when running locally.
---
📁 Project Structure
```
fireshield-ai/
├── 📱 mobile/                    # Flutter Mobile App
│   ├── lib/
│   │   ├── main.dart             # App entry point
│   │   ├── core/
│   │   │   ├── theme/            # Material 3 theme, colors
│   │   │   ├── constants/        # API endpoints, app constants
│   │   │   ├── services/         # API, location, storage services
│   │   │   ├── providers/        # Riverpod state providers
│   │   │   └── utils/            # Validators, extensions
│   │   ├── features/
│   │   │   ├── auth/             # Login, register, splash, onboarding
│   │   │   ├── home/             # Home screen, SOS button, quick actions
│   │   │   ├── sos/              # SOS reporting, media upload, AI analysis
│   │   │   ├── chatbot/          # Emergency chatbot interface
│   │   │   ├── map/              # Nearby services map
│   │   │   ├── incidents/        # Incident history and details
│   │   │   ├── profile/          # User profile
│   │   │   └── settings/         # App settings
│   │   ├── shared/
│   │   │   ├── models/           # Data models
│   │   │   └── widgets/          # Reusable widgets
│   │   └── l10n/                 # Localization (EN, HI)
│   └── pubspec.yaml
│
├── 🖥️ dashboard/                 # Web Dashboard
│   ├── index.html                # Main HTML
│   ├── css/
│   │   ├── styles.css            # Core styles
│   │   └── animations.css        # Animation keyframes
│   ├── js/
│   │   ├── app.js                # App initialization
│   │   ├── dashboard.js          # Dashboard view
│   │   ├── map.js                # Live map view
│   │   ├── incidents.js          # Incident management
│   │   ├── analytics.js          # Analytics charts
│   │   ├── teams.js              # Team management
│   │   ├── api.js                # API service
│   │   └── data.js               # Sample data
│   └── assets/                   # Static assets
│
├── ⚙️ backend/                   # FastAPI Backend
│   ├── app/
│   │   ├── main.py               # FastAPI app
│   │   ├── config.py             # Settings
│   │   ├── models/               # Pydantic models
│   │   ├── routes/               # API route handlers
│   │   ├── services/             # Business logic
│   │   └── utils/                # Helpers
│   ├── requirements.txt
│   ├── runtime.txt               # Pinned Python version for deployment
│   ├── .env.example
│   └── run.py
│
├── 📚 docs/                      # Documentation
│   ├── architecture.md           # System architecture
│   ├── api.md                    # API documentation
│   ├── firebase-schema.md        # Database schema
│   └── setup-guide.md            # Detailed setup guide
│
└── README.md                     # This file
```
---
🔥 Firebase Schema (Production Ready)
While the MVP uses in-memory storage for demo purposes, the system is designed for Firebase:
Firestore Collections
```
users/
  {userId}/
    - name: string
    - email: string
    - phone: string
    - role: "citizen" | "official" | "admin"
    - avatarUrl: string
    - createdAt: timestamp
    - emergencyContacts: array

incidents/
  {incidentId}/
    - userId: string (ref → users)
    - title: string
    - description: string
    - location: geopoint
    - address: string
    - severity: number (1-5)
    - status: string
    - mediaUrls: array
    - aiAnalysis: map
    - assignedTeam: string
    - createdAt: timestamp
    - updatedAt: timestamp
    - responseTimeMins: number
    - statusHistory: array[{status, timestamp, updatedBy}]

fire_stations/
  {stationId}/
    - name: string
    - location: geopoint
    - address: string
    - phone: string
    - availableUnits: number
    - teams: array

analytics/
  daily/{date}/
    - totalIncidents: number
    - resolvedIncidents: number
    - avgResponseTime: number
    - incidentsBySeverity: map
```
---
🌐 Deployment
This project is currently deployed using:
Backend → Render (free tier, Python web service)
Dashboard → Vercel (free tier, static hosting)
Backend (Alternative Production Options)
```bash
# Using Docker
docker build -t fireshield-api .
docker run -p 8000:8000 fireshield-api

# Using Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```
Dashboard (Alternative Hosting Options)
```bash
# Deploy to Firebase Hosting
firebase init hosting
firebase deploy

# Or any static hosting (Vercel, Netlify, GitHub Pages)
```
Mobile App
```bash
# Android APK
flutter build apk --release

# iOS
flutter build ios --release

# App Bundle (Play Store)
flutter build appbundle --release
```
---
🏆 Innovation Highlights
AI-Powered Severity Assessment — Automated fire classification and risk scoring
Intelligent Chatbot — Real-time emergency guidance in multiple languages
One-Tap SOS — Fastest possible emergency reporting with auto-captured context
Real-Time Command Center — Live map, analytics, and dispatch capabilities
Predictive Heatmaps — Identify fire-prone areas for preventive measures
Scalable Architecture — Designed for NDMA/municipal adoption across India
Offline Resilience — Critical features work without internet
Multilingual — Hindi and English for pan-India coverage
---
📄 License
This project is built for the National Hackathon and is open for educational and governmental adoption.
---
👥 Team
Built with ❤️ for India's safety.
Theme: "The Last-Minute Life Saver"
---
<p align="center">
  <strong>🔥 FireShield AI — Because Every Second Counts 🔥</strong>
</p>
