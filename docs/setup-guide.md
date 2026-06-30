# FireShield AI — Detailed Setup Guide

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Backend Setup](#backend-setup)
3. [Dashboard Setup](#dashboard-setup)
4. [Mobile App Setup](#mobile-app-setup)
5. [Firebase Setup (Production)](#firebase-setup)
6. [Google Maps Setup](#google-maps-setup)
7. [Gemini AI Setup](#gemini-ai-setup)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites {#prerequisites}

### Required Software

| Software | Version | Download |
|----------|---------|----------|
| Python | 3.9+ | [python.org](https://www.python.org/downloads/) |
| Flutter SDK | 3.x | [flutter.dev](https://flutter.dev/docs/get-started/install) |
| Git | Latest | [git-scm.com](https://git-scm.com/downloads) |
| VS Code or Android Studio | Latest | [code.visualstudio.com](https://code.visualstudio.com/) |
| Chrome/Edge/Firefox | Latest | For dashboard |

### Optional (for Production)

| Software | Purpose |
|----------|---------|
| Docker | Container deployment |
| Firebase CLI | Firebase deployment |
| Node.js 18+ | For Firebase CLI |

### Verify Installation

```bash
# Check Python
python --version  # Should be 3.9+

# Check Flutter
flutter --version  # Should be 3.x
flutter doctor      # Should show no critical issues

# Check Git
git --version
```

---

## Backend Setup {#backend-setup}

### Step 1: Navigate to Backend

```bash
cd fireshield-ai/backend
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
# Copy the example env file
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

Edit `.env` with your settings:

```env
SECRET_KEY=your-secret-key-at-least-32-characters-long
GEMINI_API_KEY=your-gemini-api-key-optional
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=*
```

> **Note:** The backend works without a Gemini API key — it uses a realistic simulation.

### Step 5: Run the Server

```bash
python run.py
```

You should see:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Application startup complete.
```

### Step 6: Verify

- Open **http://localhost:8000** — Should show API info
- Open **http://localhost:8000/docs** — Swagger UI with all endpoints
- Open **http://localhost:8000/redoc** — ReDoc documentation

### Test the API

```bash
# Login with demo account
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "citizen@demo.com", "password": "demo123"}'

# Get incidents
curl http://localhost:8000/api/incidents

# Get analytics
curl http://localhost:8000/api/analytics/summary
```

---

## Dashboard Setup {#dashboard-setup}

### Option 1: Direct File (Simplest)

Just double-click `dashboard/index.html` or:

```bash
# Windows
start dashboard\index.html

# macOS
open dashboard/index.html

# Linux
xdg-open dashboard/index.html
```

### Option 2: Local HTTP Server (Recommended)

```bash
# Using Python
cd fireshield-ai/dashboard
python -m http.server 3000

# Then open http://localhost:3000
```

### Option 3: Using VS Code Live Server

1. Install the "Live Server" extension in VS Code
2. Right-click `dashboard/index.html`
3. Select "Open with Live Server"

### Configuration

The dashboard connects to the backend at `http://localhost:8000`. If your backend runs on a different port, edit the `API_BASE_URL` in `dashboard/js/api.js`.

> **Important:** The dashboard works completely with built-in sample data even without the backend running!

---

## Mobile App Setup {#mobile-app-setup}

### Step 1: Verify Flutter

```bash
flutter doctor
```

Ensure you see checkmarks for:
- Flutter SDK
- Android toolchain (for Android development)
- Android Studio / VS Code
- Connected device / emulator

### Step 2: Navigate to Mobile

```bash
cd fireshield-ai/mobile
```

### Step 3: Get Dependencies

```bash
flutter pub get
```

### Step 4: Configure API URL

Edit `lib/core/constants/app_constants.dart`:

```dart
// For Android Emulator (connects to host machine)
static const String apiBaseUrl = 'http://10.0.2.2:8000';

// For iOS Simulator
// static const String apiBaseUrl = 'http://localhost:8000';

// For Physical Device (use your computer's IP)
// static const String apiBaseUrl = 'http://192.168.x.x:8000';
```

### Step 5: Run the App

```bash
# Run on connected device/emulator
flutter run

# Run on specific device
flutter devices          # List available devices
flutter run -d <device>  # Run on specific device

# Run in debug mode with hot reload
flutter run --debug
```

### Step 6: Build Release APK

```bash
# Build APK
flutter build apk --release

# The APK will be at:
# build/app/outputs/flutter-apk/app-release.apk

# Build App Bundle (for Play Store)
flutter build appbundle --release
```

### Google Maps Configuration (Optional)

The app includes a fallback list view without Google Maps. To enable maps:

1. Get a Google Maps API key from [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Maps SDK for Android and iOS

**Android:** Edit `android/app/src/main/AndroidManifest.xml`:
```xml
<application>
    <meta-data
        android:name="com.google.android.geo.API_KEY"
        android:value="YOUR_GOOGLE_MAPS_API_KEY"/>
</application>
```

**iOS:** Edit `ios/Runner/AppDelegate.swift`:
```swift
import GoogleMaps

@UIApplicationMain
class AppDelegate: FlutterAppDelegate {
  override func application(...) -> Bool {
    GMSServices.provideAPIKey("YOUR_GOOGLE_MAPS_API_KEY")
    // ...
  }
}
```

---

## Firebase Setup (Production) {#firebase-setup}

### Step 1: Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add Project"
3. Name: "FireShield AI"
4. Enable Google Analytics (optional)

### Step 2: Enable Services

**Authentication:**
1. Authentication → Sign-in method
2. Enable Email/Password
3. Enable Phone Authentication (for OTP)

**Firestore:**
1. Firestore Database → Create Database
2. Start in test mode (configure rules later)
3. Choose region: `asia-south1` (Mumbai)

**Storage:**
1. Storage → Get Started
2. Configure security rules

**Cloud Messaging:**
1. Cloud Messaging → Enable
2. Generate Web Push certificate

### Step 3: Add Firebase to Flutter

```bash
# Install FlutterFire CLI
dart pub global activate flutterfire_cli

# Configure Firebase
flutterfire configure --project=your-project-id
```

### Step 4: Configure Security Rules

See `docs/firebase-schema.md` for complete security rules.

---

## Gemini AI Setup {#gemini-ai-setup}

### For Production AI Analysis

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Create an API key
3. Add to `.env`:
   ```
   GEMINI_API_KEY=your-api-key-here
   ```

### For Demo (Default)

The backend includes a sophisticated AI simulation that works without an API key. It analyzes incident descriptions, categories, and context to generate realistic severity assessments.

---

## Troubleshooting {#troubleshooting}

### Backend Issues

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` in activated venv |
| Port 8000 in use | Change port in `.env` or `run.py` |
| CORS errors | Ensure CORS_ORIGINS=* in `.env` |
| Import errors | Ensure you're running from the `backend/` directory |

### Flutter Issues

| Issue | Solution |
|-------|----------|
| `pub get` fails | Run `flutter clean` then `flutter pub get` |
| Build errors | Run `flutter doctor` and fix issues |
| API connection refused | Check API URL matches your setup (10.0.2.2 for emulator) |
| Google Maps blank | Add API key to AndroidManifest.xml |
| Permission denied (location) | Grant location permission in device settings |

### Dashboard Issues

| Issue | Solution |
|-------|----------|
| Charts not loading | Check internet connection (Chart.js loads from CDN) |
| Map not showing | Check internet connection (Leaflet tiles load from CDN) |
| API data not loading | Start the backend server first |
| Layout broken | Use a modern browser (Chrome/Firefox/Edge) |

### General

```bash
# Reset Flutter
flutter clean
flutter pub get

# Reset Python
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## Quick Demo Checklist

- [ ] Start backend: `cd backend && python run.py`
- [ ] Open dashboard: `http://localhost:3000` (or open `dashboard/index.html`)
- [ ] Login to dashboard with `official@demo.com / demo123`
- [ ] Start mobile app: `cd mobile && flutter run`
- [ ] Login to mobile app with `citizen@demo.com / demo123`
- [ ] Trigger SOS from mobile app
- [ ] See real-time alert on dashboard
- [ ] Test chatbot with emergency questions
- [ ] View analytics and heatmap on dashboard
