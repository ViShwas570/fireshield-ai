class AppConstants {
  static const appName = 'FireShield AI';
  static const appVersion = '1.0.0';

  // API - Change to your backend URL
  // For Android emulator: http://10.0.2.2:8000
  // For iOS simulator: http://localhost:8000
  // For physical device: use your computer's IP
  static const apiBaseUrl = 'http://10.0.2.2:8000';

  // Emergency Numbers (India)
  static const emergencyNumbers = {
    '🚒 Fire': '101',
    '📱 Emergency': '112',
    '🚑 Ambulance': '108',
    '🚔 Police': '100',
  };

  // Map defaults (Center of India)
  static const defaultLat = 20.5937;
  static const defaultLng = 78.9629;

  // API Endpoints
  static const loginUrl = '/api/auth/login';
  static const registerUrl = '/api/auth/register';
  static const profileUrl = '/api/auth/profile';
  static const incidentsUrl = '/api/incidents';
  static const sosUrl = '/api/emergency/sos';
  static const chatUrl = '/api/chatbot/message';
  static const nearbyFireStationsUrl = '/api/nearby/fire-stations';
  static const nearbyHospitalsUrl = '/api/nearby/hospitals';
  static const nearbyPoliceUrl = '/api/nearby/police';
  static const analyticsUrl = '/api/analytics/summary';
}
