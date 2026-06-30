import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../shared/models/incident_model.dart';
import '../constants/api_endpoints.dart';
import '../services/api_service.dart';
import 'auth_provider.dart';

// Incidents state
class IncidentsState {
  final List<IncidentModel> incidents;
  final bool isLoading;
  final String? error;
  final String filter;

  const IncidentsState({
    this.incidents = const [],
    this.isLoading = false,
    this.error,
    this.filter = 'all',
  });

  IncidentsState copyWith({
    List<IncidentModel>? incidents,
    bool? isLoading,
    String? error,
    String? filter,
  }) {
    return IncidentsState(
      incidents: incidents ?? this.incidents,
      isLoading: isLoading ?? this.isLoading,
      error: error,
      filter: filter ?? this.filter,
    );
  }

  List<IncidentModel> get filteredIncidents {
    switch (filter) {
      case 'active':
        return incidents.where((i) => i.isActive).toList();
      case 'resolved':
        return incidents.where((i) => i.isResolved).toList();
      default:
        return incidents;
    }
  }
}

class IncidentsNotifier extends StateNotifier<IncidentsState> {
  final ApiService _api;

  IncidentsNotifier(this._api) : super(const IncidentsState()) {
    loadIncidents();
  }

  Future<void> loadIncidents() async {
    state = state.copyWith(isLoading: true, error: null);
    try {
      final response = await _api.get(ApiEndpoints.myIncidents);
      final data = response.data;
      List<IncidentModel> incidents;

      if (data is List) {
        incidents = data.map((e) => IncidentModel.fromJson(e as Map<String, dynamic>)).toList();
      } else if (data is Map && data['incidents'] is List) {
        incidents = (data['incidents'] as List)
            .map((e) => IncidentModel.fromJson(e as Map<String, dynamic>))
            .toList();
      } else {
        incidents = IncidentModel.demoList();
      }

      state = state.copyWith(incidents: incidents, isLoading: false);
    } on DioException {
      // Use demo data on failure
      state = state.copyWith(
        incidents: IncidentModel.demoList(),
        isLoading: false,
      );
    } catch (e) {
      state = state.copyWith(
        incidents: IncidentModel.demoList(),
        isLoading: false,
      );
    }
  }

  void setFilter(String filter) {
    state = state.copyWith(filter: filter);
  }

  Future<IncidentModel?> createIncident({
    required String title,
    required String description,
    required String category,
    required double latitude,
    required double longitude,
    required String address,
    int severity = 3,
    List<String>? mediaUrls,
  }) async {
    try {
      final response = await _api.post(
        ApiEndpoints.incidents,
        data: {
          'title': title,
          'description': description,
          'category': category,
          'latitude': latitude,
          'longitude': longitude,
          'address': address,
          'severity': severity,
          'media_urls': mediaUrls ?? [],
        },
      );

      final incident = IncidentModel.fromJson(response.data as Map<String, dynamic>);
      state = state.copyWith(
        incidents: [incident, ...state.incidents],
      );
      return incident;
    } on DioException {
      // Create local incident on failure
      final incident = IncidentModel(
        id: 'INC-${DateTime.now().millisecondsSinceEpoch}',
        title: title,
        description: description,
        category: category,
        severity: severity,
        status: 'reported',
        latitude: latitude,
        longitude: longitude,
        address: address,
        createdAt: DateTime.now(),
        mediaUrls: mediaUrls ?? [],
      );
      state = state.copyWith(
        incidents: [incident, ...state.incidents],
      );
      return incident;
    } catch (e) {
      return null;
    }
  }

  Future<Map<String, dynamic>?> analyzeWithAI({
    required String description,
    required String category,
    String? imagePath,
  }) async {
    try {
      final response = await _api.post(
        ApiEndpoints.sosAnalyze,
        data: {
          'description': description,
          'category': category,
          'image_path': imagePath,
        },
      );
      return response.data as Map<String, dynamic>;
    } catch (e) {
      // Return demo AI analysis
      return {
        'severity_score': category == 'Forest' ? 4 : 3,
        'risk_level': category == 'Forest' ? 'High' : 'Moderate',
        'fire_type': category,
        'spread_risk': category == 'Forest' || category == 'Industrial' ? 'High' : 'Low',
        'recommended_response': category == 'Forest'
            ? '3 fire engines, aerial support'
            : '1 fire engine, rescue team',
        'confidence': 0.85,
        'safety_tips': [
          'Evacuate the area immediately',
          'Stay low to avoid smoke inhalation',
          'Call 101 for fire service',
        ],
      };
    }
  }
}

final incidentsProvider =
    StateNotifierProvider<IncidentsNotifier, IncidentsState>((ref) {
  final api = ref.watch(apiServiceProvider);
  return IncidentsNotifier(api);
});

// Single incident provider
final incidentDetailProvider =
    FutureProvider.family<IncidentModel?, String>((ref, id) async {
  final incidentsState = ref.read(incidentsProvider);
  // Try to find in local list first
  final local = incidentsState.incidents.where((i) => i.id == id);
  if (local.isNotEmpty) return local.first;

  // Otherwise fetch from API
  try {
    final api = ref.read(apiServiceProvider);
    final response = await api.get(ApiEndpoints.incidentById(id));
    return IncidentModel.fromJson(response.data as Map<String, dynamic>);
  } catch (e) {
    // Return first demo if available
    final demos = IncidentModel.demoList();
    final match = demos.where((i) => i.id == id);
    return match.isNotEmpty ? match.first : demos.first;
  }
});
