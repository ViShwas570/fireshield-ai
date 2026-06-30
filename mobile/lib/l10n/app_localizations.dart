import 'app_en.dart';
import 'app_hi.dart';

class AppLocalizations {
  static String _currentLocale = 'en';

  static String get currentLocale => _currentLocale;

  static void setLocale(String locale) {
    _currentLocale = locale;
  }

  static String tr(String key) {
    final Map<String, String> strings;
    switch (_currentLocale) {
      case 'hi':
        strings = hiStrings;
        break;
      default:
        strings = enStrings;
    }
    return strings[key] ?? enStrings[key] ?? key;
  }

  static String get appName => tr('app_name');
  static String get appTagline => tr('app_tagline');

  // Convenience getters for commonly used strings
  static String get login => tr('login');
  static String get register => tr('register');
  static String get logout => tr('logout');
  static String get home => tr('home');
  static String get map => tr('map');
  static String get chatbot => tr('chatbot');
  static String get incidents => tr('incidents');
  static String get profile => tr('profile');
  static String get settings => tr('settings');
  static String get sosButton => tr('sos_button');

  static String greeting() {
    final hour = DateTime.now().hour;
    if (hour < 12) return tr('greeting_morning');
    if (hour < 17) return tr('greeting_afternoon');
    return tr('greeting_evening');
  }
}
