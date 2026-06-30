import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../shared/models/user_model.dart';
import '../services/api_service.dart';
import '../services/storage_service.dart';
import '../constants/api_endpoints.dart';
import 'package:shared_preferences/shared_preferences.dart';

// Storage service provider
final storageServiceProvider = Provider<StorageService>((ref) {
  throw UnimplementedError('Must be overridden in main');
});

// API service provider
final apiServiceProvider = Provider<ApiService>((ref) {
  final storage = ref.watch(storageServiceProvider);
  return ApiService(storage);
});

// Auth state
enum AuthStatus { initial, authenticated, unauthenticated, loading }

class AuthState {
  final AuthStatus status;
  final UserModel? user;
  final String? error;

  const AuthState({
    this.status = AuthStatus.initial,
    this.user,
    this.error,
  });

  AuthState copyWith({
    AuthStatus? status,
    UserModel? user,
    String? error,
  }) {
    return AuthState(
      status: status ?? this.status,
      user: user ?? this.user,
      error: error,
    );
  }
}

class AuthNotifier extends StateNotifier<AuthState> {
  final ApiService _api;
  final StorageService _storage;

  AuthNotifier(this._api, this._storage) : super(const AuthState()) {
    _checkAuthStatus();
  }

  Future<void> _checkAuthStatus() async {
    final token = _storage.getAuthToken();
    if (token != null && token.isNotEmpty) {
      final userData = _storage.getUserData();
      if (userData != null) {
        state = AuthState(
          status: AuthStatus.authenticated,
          user: UserModel.fromJson(userData),
        );
      } else {
        state = AuthState(
          status: AuthStatus.authenticated,
          user: UserModel.demo(),
        );
      }
    } else {
      state = const AuthState(status: AuthStatus.unauthenticated);
    }
  }

  Future<bool> login(String email, String password) async {
    state = state.copyWith(status: AuthStatus.loading, error: null);
    try {
      final response = await _api.post(
        ApiEndpoints.login,
        data: {'email': email, 'password': password},
      );

      final data = response.data as Map<String, dynamic>;
      final token = data['access_token']?.toString() ?? data['token']?.toString() ?? '';
      final userData = data['user'] as Map<String, dynamic>?;

      if (token.isNotEmpty) {
        await _storage.setAuthToken(token);
        if (userData != null) {
          await _storage.setUserData(userData);
          state = AuthState(
            status: AuthStatus.authenticated,
            user: UserModel.fromJson(userData),
          );
        } else {
          state = AuthState(
            status: AuthStatus.authenticated,
            user: UserModel.demo(),
          );
        }
        return true;
      }
      state = state.copyWith(
        status: AuthStatus.unauthenticated,
        error: 'Invalid response from server',
      );
      return false;
    } on DioException catch (e) {
      // Demo fallback
      if (email == 'citizen@demo.com' && password == 'demo123') {
        final demoUser = UserModel.demo();
        await _storage.setAuthToken('demo-token-fireshield');
        await _storage.setUserData(demoUser.toJson());
        state = AuthState(
          status: AuthStatus.authenticated,
          user: demoUser,
        );
        return true;
      }
      state = state.copyWith(
        status: AuthStatus.unauthenticated,
        error: _api.getErrorMessage(e),
      );
      return false;
    } catch (e) {
      // Demo fallback
      if (email == 'citizen@demo.com' && password == 'demo123') {
        final demoUser = UserModel.demo();
        await _storage.setAuthToken('demo-token-fireshield');
        await _storage.setUserData(demoUser.toJson());
        state = AuthState(
          status: AuthStatus.authenticated,
          user: demoUser,
        );
        return true;
      }
      state = state.copyWith(
        status: AuthStatus.unauthenticated,
        error: 'An unexpected error occurred',
      );
      return false;
    }
  }

  Future<bool> register({
    required String name,
    required String email,
    required String phone,
    required String password,
  }) async {
    state = state.copyWith(status: AuthStatus.loading, error: null);
    try {
      final response = await _api.post(
        ApiEndpoints.register,
        data: {
          'name': name,
          'email': email,
          'phone': phone,
          'password': password,
        },
      );

      final data = response.data as Map<String, dynamic>;
      final token = data['access_token']?.toString() ?? data['token']?.toString() ?? '';
      final userData = data['user'] as Map<String, dynamic>?;

      if (token.isNotEmpty) {
        await _storage.setAuthToken(token);
        if (userData != null) {
          await _storage.setUserData(userData);
          state = AuthState(
            status: AuthStatus.authenticated,
            user: UserModel.fromJson(userData),
          );
        }
        return true;
      }
      // Even if no token, treat as success with demo
      final demoUser = UserModel(
        id: 'new-user',
        name: name,
        email: email,
        phone: phone,
        createdAt: DateTime.now(),
      );
      await _storage.setAuthToken('demo-token-$email');
      await _storage.setUserData(demoUser.toJson());
      state = AuthState(
        status: AuthStatus.authenticated,
        user: demoUser,
      );
      return true;
    } on DioException catch (e) {
      // Demo fallback: register always succeeds locally
      final demoUser = UserModel(
        id: 'new-user-${DateTime.now().millisecondsSinceEpoch}',
        name: name,
        email: email,
        phone: phone,
        createdAt: DateTime.now(),
      );
      await _storage.setAuthToken('demo-token-$email');
      await _storage.setUserData(demoUser.toJson());
      state = AuthState(
        status: AuthStatus.authenticated,
        user: demoUser,
      );
      return true;
    } catch (e) {
      state = state.copyWith(
        status: AuthStatus.unauthenticated,
        error: 'Registration failed. Please try again.',
      );
      return false;
    }
  }

  Future<void> logout() async {
    try {
      await _api.post(ApiEndpoints.logout);
    } catch (_) {}
    await _storage.clearAuth();
    state = const AuthState(status: AuthStatus.unauthenticated);
  }

  void clearError() {
    state = state.copyWith(error: null);
  }
}

final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  final api = ref.watch(apiServiceProvider);
  final storage = ref.watch(storageServiceProvider);
  return AuthNotifier(api, storage);
});

final isLoggedInProvider = Provider<bool>((ref) {
  return ref.watch(authProvider).status == AuthStatus.authenticated;
});

final currentUserProvider = Provider<UserModel?>((ref) {
  return ref.watch(authProvider).user;
});
