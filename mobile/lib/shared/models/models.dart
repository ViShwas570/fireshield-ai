class UserModel {
  final String id;
  final String name;
  final String email;
  final String phone;
  final String role;
  final String? avatarUrl;
  final String createdAt;

  UserModel({
    required this.id,
    required this.name,
    required this.email,
    this.phone = '',
    this.role = 'citizen',
    this.avatarUrl,
    this.createdAt = '',
  });

  factory UserModel.fromJson(Map<String, dynamic> json) => UserModel(
        id: json['id'] ?? '',
        name: json['name'] ?? '',
        email: json['email'] ?? '',
        phone: json['phone'] ?? '',
        role: json['role'] ?? 'citizen',
        avatarUrl: json['avatar_url'],
        createdAt: json['created_at'] ?? '',
      );

  Map<String, dynamic> toJson() => {
        'id': id, 'name': name, 'email': email,
        'phone': phone, 'role': role,
        'avatar_url': avatarUrl, 'created_at': createdAt,
      };
}

class IncidentModel {
  final String id;
  final String userId;
  final String userName;
  final String title;
  final String description;
  final double latitude;
  final double longitude;
  final String address;
  final String category;
  final int severity;
  final String status;
  final List<String> mediaUrls;
  final Map<String, dynamic>? aiAnalysis;
  final String? assignedTeam;
  final String createdAt;
  final String updatedAt;
  final double? responseTimeMins;

  IncidentModel({
    required this.id,
    required this.userId,
    this.userName = '',
    required this.title,
    this.description = '',
    required this.latitude,
    required this.longitude,
    this.address = '',
    this.category = 'other',
    this.severity = 0,
    this.status = 'reported',
    this.mediaUrls = const [],
    this.aiAnalysis,
    this.assignedTeam,
    this.createdAt = '',
    this.updatedAt = '',
    this.responseTimeMins,
  });

  factory IncidentModel.fromJson(Map<String, dynamic> json) => IncidentModel(
        id: json['id'] ?? '',
        userId: json['user_id'] ?? '',
        userName: json['user_name'] ?? '',
        title: json['title'] ?? '',
        description: json['description'] ?? '',
        latitude: (json['latitude'] ?? 0).toDouble(),
        longitude: (json['longitude'] ?? 0).toDouble(),
        address: json['address'] ?? '',
        category: json['category'] ?? 'other',
        severity: json['severity'] ?? 0,
        status: json['status'] ?? 'reported',
        mediaUrls: List<String>.from(json['media_urls'] ?? []),
        aiAnalysis: json['ai_analysis'],
        assignedTeam: json['assigned_team'],
        createdAt: json['created_at'] ?? '',
        updatedAt: json['updated_at'] ?? '',
        responseTimeMins: json['response_time_mins']?.toDouble(),
      );

  String get statusDisplay => status.replaceAll('_', ' ').toUpperCase();
  String get categoryDisplay => category.replaceAll('_', ' ');

  String get timeAgo {
    try {
      final dt = DateTime.parse(createdAt);
      final diff = DateTime.now().toUtc().difference(dt);
      if (diff.inMinutes < 60) return '${diff.inMinutes}m ago';
      if (diff.inHours < 24) return '${diff.inHours}h ago';
      return '${diff.inDays}d ago';
    } catch (_) {
      return createdAt;
    }
  }
}

class ChatMessage {
  final String text;
  final bool isUser;
  final DateTime timestamp;
  final List<String> suggestions;

  ChatMessage({
    required this.text,
    required this.isUser,
    DateTime? timestamp,
    this.suggestions = const [],
  }) : timestamp = timestamp ?? DateTime.now();
}

class NearbyServiceModel {
  final String id;
  final String name;
  final double latitude;
  final double longitude;
  final String address;
  final String phone;
  final double distanceKm;
  final String serviceType;

  NearbyServiceModel({
    required this.id,
    required this.name,
    required this.latitude,
    required this.longitude,
    this.address = '',
    this.phone = '',
    this.distanceKm = 0,
    this.serviceType = '',
  });

  factory NearbyServiceModel.fromJson(Map<String, dynamic> json) =>
      NearbyServiceModel(
        id: json['id'] ?? '',
        name: json['name'] ?? '',
        latitude: (json['latitude'] ?? 0).toDouble(),
        longitude: (json['longitude'] ?? 0).toDouble(),
        address: json['address'] ?? '',
        phone: json['phone'] ?? '',
        distanceKm: (json['distance_km'] ?? 0).toDouble(),
        serviceType: json['service_type'] ?? '',
      );
}
