class ApiEndpoints {
  ApiEndpoints._();

  // Auth
  static const String login = '/api/auth/login';
  static const String register = '/api/auth/register';
  static const String logout = '/api/auth/logout';
  static const String profile = '/api/auth/profile';
  static const String refreshToken = '/api/auth/refresh';

  // Incidents
  static const String incidents = '/api/incidents';
  static String incidentById(String id) => '/api/incidents/$id';
  static String incidentStatus(String id) => '/api/incidents/$id/status';
  static const String myIncidents = '/api/incidents/my';

  // SOS
  static const String sos = '/api/sos';
  static const String sosAnalyze = '/api/sos/analyze';
  static const String sosQuick = '/api/sos/quick';

  // Chatbot
  static const String chatbot = '/api/chatbot/message';
  static const String chatHistory = '/api/chatbot/history';

  // Nearby Services
  static const String nearbyServices = '/api/services/nearby';
  static const String fireStations = '/api/services/fire-stations';
  static const String hospitals = '/api/services/hospitals';
  static const String police = '/api/services/police';

  // AI Analysis
  static const String analyzeImage = '/api/ai/analyze-image';
  static const String analyzeSeverity = '/api/ai/severity';

  // Upload
  static const String upload = '/api/upload';
}
