import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:fireshield_ai/core/theme/app_theme.dart';
import 'package:fireshield_ai/core/services/api_service.dart';
import 'package:fireshield_ai/core/constants/app_constants.dart';
import 'package:fireshield_ai/shared/models/models.dart';
import 'package:fireshield_ai/shared/widgets/widgets.dart';
import 'package:fireshield_ai/features/auth/screens/auth_screens.dart';
import 'package:fireshield_ai/features/home/screens/home_screen.dart';
import 'package:fireshield_ai/features/screens.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp]);
  SystemChrome.setSystemUIOverlayStyle(const SystemUiOverlayStyle(
    statusBarColor: Colors.transparent,
    statusBarIconBrightness: Brightness.light,
  ));
  runApp(const ProviderScope(child: FireShieldApp()));
}

// ─── Riverpod Providers ──────────────────────────────────
final themeProvider = StateProvider<ThemeMode>((ref) => ThemeMode.dark);
final authStateProvider = StateProvider<UserModel?>((ref) => null);
final incidentsProvider = StateProvider<List<IncidentModel>>((ref) => []);

// ─── Main App ────────────────────────────────────────────
class FireShieldApp extends ConsumerWidget {
  const FireShieldApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final themeMode = ref.watch(themeProvider);
    return MaterialApp(
      title: AppConstants.appName,
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: themeMode,
      home: const AppNavigator(),
    );
  }
}

// ─── Navigation Controller ───────────────────────────────
class AppNavigator extends ConsumerStatefulWidget {
  const AppNavigator({super.key});

  @override
  ConsumerState<AppNavigator> createState() => _AppNavigatorState();
}

class _AppNavigatorState extends ConsumerState<AppNavigator> {
  final _api = ApiService();
  String _currentScreen = 'splash';
  int _bottomNavIndex = 0;

  @override
  void initState() {
    super.initState();
    // Show splash then login
    Future.delayed(const Duration(milliseconds: 2500), () {
      if (mounted) setState(() => _currentScreen = 'login');
    });
  }

  // ─── API Methods ─────────────────────────────────────
  Future<void> _login(String email, String password) async {
    try {
      final response = await _api.post(
        AppConstants.loginUrl,
        data: {'email': email, 'password': password},
      );
      final data = response.data;
      _api.setToken(data['access_token']);
      final user = UserModel.fromJson(data['user']);
      ref.read(authStateProvider.notifier).state = user;
      await _loadIncidents();
      setState(() => _currentScreen = 'home');
    } catch (e) {
      throw Exception(e.toString());
    }
  }

  Future<void> _register(String name, String email, String phone, String password) async {
    try {
      final response = await _api.post(
        AppConstants.registerUrl,
        data: {'name': name, 'email': email, 'phone': phone, 'password': password},
      );
      final data = response.data;
      _api.setToken(data['access_token']);
      final user = UserModel.fromJson(data['user']);
      ref.read(authStateProvider.notifier).state = user;
      setState(() => _currentScreen = 'home');
    } catch (e) {
      throw Exception(e.toString());
    }
  }

  Future<void> _loadIncidents() async {
    try {
      final response = await _api.get(AppConstants.incidentsUrl);
      final data = response.data;
      final incidents = (data['incidents'] as List)
          .map((e) => IncidentModel.fromJson(e))
          .toList();
      ref.read(incidentsProvider.notifier).state = incidents;
    } catch (_) {}
  }

  Future<Map<String, dynamic>?> _submitSOS(String description, String category) async {
    try {
      final response = await _api.post(
        AppConstants.sosUrl,
        data: {
          'description': description,
          'latitude': 28.6139,  // Default Delhi coords for demo
          'longitude': 77.2090,
          'media_urls': [],
        },
      );
      await _loadIncidents();
      return response.data;
    } catch (e) {
      throw Exception(e.toString());
    }
  }

  Future<Map<String, dynamic>> _sendChatMessage(String message, String lang) async {
    try {
      final response = await _api.post(
        AppConstants.chatUrl,
        data: {'message': message, 'lang': lang},
      );
      return response.data;
    } catch (e) {
      return {
        'response': 'Connection error. Emergency numbers:\n🚒 Fire: 101\n📱 Emergency: 112\n🚑 Ambulance: 108',
        'suggestions': ['Call 101', 'Evacuation guide'],
      };
    }
  }

  Future<List<NearbyServiceModel>> _fetchNearby(String type) async {
    try {
      final endpoints = {
        'fire_station': AppConstants.nearbyFireStationsUrl,
        'hospital': AppConstants.nearbyHospitalsUrl,
        'police': AppConstants.nearbyPoliceUrl,
      };
      final response = await _api.get(
        endpoints[type]!,
        params: {'lat': 28.6139, 'lng': 77.2090, 'radius': 50},
      );
      return (response.data as List)
          .map((e) => NearbyServiceModel.fromJson(e))
          .toList();
    } catch (_) {
      return [];
    }
  }

  void _logout() {
    _api.clearToken();
    ref.read(authStateProvider.notifier).state = null;
    ref.read(incidentsProvider.notifier).state = [];
    setState(() {
      _currentScreen = 'login';
      _bottomNavIndex = 0;
    });
  }

  // ─── Build ───────────────────────────────────────────
  @override
  Widget build(BuildContext context) {
    final user = ref.watch(authStateProvider);
    final incidents = ref.watch(incidentsProvider);

    switch (_currentScreen) {
      case 'splash':
        return SplashScreen(
          onComplete: () => setState(() => _currentScreen = 'login'),
        );

      case 'login':
        return LoginScreen(
          onLogin: _login,
          onRegister: () => setState(() => _currentScreen = 'register'),
        );

      case 'register':
        return RegisterScreen(
          onRegister: _register,
          onBack: () => setState(() => _currentScreen = 'login'),
        );

      case 'sos':
        return SOSScreen(onSubmitSOS: _submitSOS);

      case 'chatbot':
        return ChatbotScreen(onSendMessage: _sendChatMessage);

      case 'map':
        return NearbyServicesScreen(fetchNearby: _fetchNearby);

      case 'incidents':
        return IncidentsListScreen(
          incidents: incidents,
          onTap: (inc) {},
        );

      case 'profile':
        return ProfileScreen(
          user: user,
          totalReports: incidents.length,
          onLogout: _logout,
          onSettings: () => setState(() => _currentScreen = 'settings'),
        );

      case 'settings':
        return SettingsScreen(
          isDarkMode: ref.watch(themeProvider) == ThemeMode.dark,
          onThemeChanged: (isDark) {
            ref.read(themeProvider.notifier).state =
                isDark ? ThemeMode.dark : ThemeMode.light;
          },
        );

      case 'home':
      default:
        return _buildHomeWithNav(user, incidents);
    }
  }

  Widget _buildHomeWithNav(UserModel? user, List<IncidentModel> incidents) {
    final screens = [
      HomeScreen(
        user: user,
        recentIncidents: incidents,
        onSOS: () => setState(() => _currentScreen = 'sos'),
        onChat: () => setState(() => _currentScreen = 'chatbot'),
        onMap: () => setState(() => _currentScreen = 'map'),
        onIncidents: () => setState(() => _currentScreen = 'incidents'),
        onProfile: () => setState(() => _currentScreen = 'profile'),
      ),
      NearbyServicesScreen(fetchNearby: _fetchNearby),
      // SOS placeholder (handled by FAB)
      const SizedBox(),
      IncidentsListScreen(
        incidents: incidents,
        onTap: (inc) {},
      ),
      ProfileScreen(
        user: user,
        totalReports: incidents.length,
        onLogout: _logout,
        onSettings: () => setState(() => _currentScreen = 'settings'),
      ),
    ];

    return Scaffold(
      body: IndexedStack(
        index: _bottomNavIndex == 2 ? 0 : _bottomNavIndex,
        children: screens,
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _bottomNavIndex,
        onDestinationSelected: (index) {
          if (index == 2) {
            setState(() => _currentScreen = 'sos');
            return;
          }
          setState(() => _bottomNavIndex = index);
        },
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home_outlined),
              selectedIcon: Icon(Icons.home), label: 'Home'),
          NavigationDestination(icon: Icon(Icons.map_outlined),
              selectedIcon: Icon(Icons.map), label: 'Map'),
          NavigationDestination(icon: Icon(Icons.emergency,
              color: AppColors.danger, size: 32), label: 'SOS'),
          NavigationDestination(icon: Icon(Icons.history_outlined),
              selectedIcon: Icon(Icons.history), label: 'History'),
          NavigationDestination(icon: Icon(Icons.person_outline),
              selectedIcon: Icon(Icons.person), label: 'Profile'),
        ],
      ),
      floatingActionButton: _bottomNavIndex == 0
          ? null
          : null, // SOS FAB handled in home
    );
  }
}
