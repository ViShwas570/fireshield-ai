import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../constants/app_constants.dart';

class StorageService {
  final SharedPreferences _prefs;

  StorageService(this._prefs);

  // Auth Token
  String? getAuthToken() => _prefs.getString(AppConstants.keyAuthToken);
  Future<bool> setAuthToken(String token) =>
      _prefs.setString(AppConstants.keyAuthToken, token);

  // Refresh Token
  String? getRefreshToken() => _prefs.getString(AppConstants.keyRefreshToken);
  Future<bool> setRefreshToken(String token) =>
      _prefs.setString(AppConstants.keyRefreshToken, token);

  // User Data
  Map<String, dynamic>? getUserData() {
    final data = _prefs.getString(AppConstants.keyUserData);
    if (data != null) {
      return json.decode(data) as Map<String, dynamic>;
    }
    return null;
  }

  Future<bool> setUserData(Map<String, dynamic> userData) =>
      _prefs.setString(AppConstants.keyUserData, json.encode(userData));

  // Theme Mode
  String getThemeMode() => _prefs.getString(AppConstants.keyThemeMode) ?? 'system';
  Future<bool> setThemeMode(String mode) =>
      _prefs.setString(AppConstants.keyThemeMode, mode);

  // Language
  String getLanguage() => _prefs.getString(AppConstants.keyLanguage) ?? 'en';
  Future<bool> setLanguage(String lang) =>
      _prefs.setString(AppConstants.keyLanguage, lang);

  // Onboarding
  bool isOnboardingComplete() =>
      _prefs.getBool(AppConstants.keyOnboardingComplete) ?? false;
  Future<bool> setOnboardingComplete(bool complete) =>
      _prefs.setBool(AppConstants.keyOnboardingComplete, complete);

  // Cached Incidents
  List<Map<String, dynamic>> getCachedIncidents() {
    final data = _prefs.getString(AppConstants.keyCachedIncidents);
    if (data != null) {
      final list = json.decode(data) as List;
      return list.cast<Map<String, dynamic>>();
    }
    return [];
  }

  Future<bool> setCachedIncidents(List<Map<String, dynamic>> incidents) =>
      _prefs.setString(AppConstants.keyCachedIncidents, json.encode(incidents));

  // Clear Auth
  Future<void> clearAuth() async {
    await _prefs.remove(AppConstants.keyAuthToken);
    await _prefs.remove(AppConstants.keyRefreshToken);
    await _prefs.remove(AppConstants.keyUserData);
  }

  // Clear All
  Future<bool> clearAll() => _prefs.clear();

  // Check if logged in
  bool isLoggedIn() {
    final token = getAuthToken();
    return token != null && token.isNotEmpty;
  }
}
