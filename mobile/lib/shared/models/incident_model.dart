class IncidentModel {
  final String id;
  final String title;
  final String description;
  final String category;
  final int severity;
  final String status;
  final double latitude;
  final double longitude;
  final String address;
  final String? reporterName;
  final String? reporterId;
  final List<String> mediaUrls;
  final Map<String, dynamic>? aiAnalysis;
  final String? assignedTeam;
  final DateTime createdAt;
  final DateTime? updatedAt;
  final List<Map<String, dynamic>>? timeline;

  const IncidentModel({
    required this.id,
    required this.title,
    required this.description,
    required this.category,
    required this.severity,
    required this.status,
    required this.latitude,
    required this.longitude,
    required this.address,
    this.reporterName,
    this.reporterId,
    this.mediaUrls = const [],
    this.aiAnalysis,
    this.assignedTeam,
    required this.createdAt,
    this.updatedAt,
    this.timeline,
  });

  factory IncidentModel.fromJson(Map<String, dynamic> json) {
    return IncidentModel(
      id: json['id']?.toString() ?? json['_id']?.toString() ?? '',
      title: json['title']?.toString() ?? 'Fire Incident',
      description: json['description']?.toString() ?? '',
      category: json['category']?.toString() ?? 'Other',
      severity: int.tryParse(json['severity']?.toString() ?? '3') ?? 3,
      status: json['status']?.toString() ?? 'reported',
      latitude: double.tryParse(json['latitude']?.toString() ?? '0') ?? 0.0,
      longitude: double.tryParse(json['longitude']?.toString() ?? '0') ?? 0.0,
      address: json['address']?.toString() ?? 'Unknown location',
      reporterName: json['reporter_name']?.toString(),
      reporterId: json['reporter_id']?.toString(),
      mediaUrls: (json['media_urls'] as List?)
              ?.map((e) => e.toString())
              .toList() ??
          [],
      aiAnalysis: json['ai_analysis'] as Map<String, dynamic>?,
      assignedTeam: json['assigned_team']?.toString(),
      createdAt: DateTime.tryParse(json['created_at']?.toString() ?? '') ??
          DateTime.now(),
      updatedAt: json['updated_at'] != null
          ? DateTime.tryParse(json['updated_at'].toString())
          : null,
      timeline: (json['timeline'] as List?)
          ?.map((e) => e as Map<String, dynamic>)
          .toList(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'description': description,
      'category': category,
      'severity': severity,
      'status': status,
      'latitude': latitude,
      'longitude': longitude,
      'address': address,
      'reporter_name': reporterName,
      'reporter_id': reporterId,
      'media_urls': mediaUrls,
      'ai_analysis': aiAnalysis,
      'assigned_team': assignedTeam,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt?.toIso8601String(),
      'timeline': timeline,
    };
  }

  IncidentModel copyWith({
    String? id,
    String? title,
    String? description,
    String? category,
    int? severity,
    String? status,
    double? latitude,
    double? longitude,
    String? address,
    String? reporterName,
    String? reporterId,
    List<String>? mediaUrls,
    Map<String, dynamic>? aiAnalysis,
    String? assignedTeam,
    DateTime? createdAt,
    DateTime? updatedAt,
    List<Map<String, dynamic>>? timeline,
  }) {
    return IncidentModel(
      id: id ?? this.id,
      title: title ?? this.title,
      description: description ?? this.description,
      category: category ?? this.category,
      severity: severity ?? this.severity,
      status: status ?? this.status,
      latitude: latitude ?? this.latitude,
      longitude: longitude ?? this.longitude,
      address: address ?? this.address,
      reporterName: reporterName ?? this.reporterName,
      reporterId: reporterId ?? this.reporterId,
      mediaUrls: mediaUrls ?? this.mediaUrls,
      aiAnalysis: aiAnalysis ?? this.aiAnalysis,
      assignedTeam: assignedTeam ?? this.assignedTeam,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
      timeline: timeline ?? this.timeline,
    );
  }

  bool get isActive =>
      status == 'reported' ||
      status == 'verified' ||
      status == 'responding' ||
      status == 'contained';

  bool get isResolved => status == 'resolved' || status == 'false_alarm';

  String get statusDisplay {
    switch (status) {
      case 'reported':
        return 'Reported';
      case 'verified':
        return 'Verified';
      case 'responding':
        return 'Responding';
      case 'contained':
        return 'Contained';
      case 'resolved':
        return 'Resolved';
      case 'false_alarm':
        return 'False Alarm';
      default:
        return status;
    }
  }

  static List<IncidentModel> demoList() {
    return [
      IncidentModel(
        id: 'INC-001',
        title: 'Building Fire - Sector 44',
        description:
            'Large fire reported in residential building on the 3rd floor. Smoke visible from distance.',
        category: 'Building',
        severity: 4,
        status: 'responding',
        latitude: 28.5355,
        longitude: 77.3910,
        address: 'Sector 44, Gurugram, Haryana',
        reporterName: 'Rahul Sharma',
        assignedTeam: 'Fire Station #12',
        createdAt: DateTime.now().subtract(const Duration(hours: 2)),
        aiAnalysis: {
          'severity_score': 4,
          'risk_level': 'High',
          'fire_type': 'Structural',
          'spread_risk': 'Moderate',
          'recommended_response': '2 fire engines, 1 ladder truck',
          'confidence': 0.87,
        },
        timeline: [
          {
            'status': 'reported',
            'time': DateTime.now()
                .subtract(const Duration(hours: 2))
                .toIso8601String(),
            'note': 'Incident reported by citizen',
          },
          {
            'status': 'verified',
            'time': DateTime.now()
                .subtract(const Duration(hours: 1, minutes: 50))
                .toIso8601String(),
            'note': 'Verified by AI analysis',
          },
          {
            'status': 'responding',
            'time': DateTime.now()
                .subtract(const Duration(hours: 1, minutes: 45))
                .toIso8601String(),
            'note': 'Fire Station #12 dispatched',
          },
        ],
      ),
      IncidentModel(
        id: 'INC-002',
        title: 'Kitchen Fire - Lajpat Nagar',
        description:
            'Small kitchen fire caused by gas leak. Contained by residents.',
        category: 'Kitchen',
        severity: 2,
        status: 'resolved',
        latitude: 28.5677,
        longitude: 77.2433,
        address: 'Lajpat Nagar, New Delhi',
        reporterName: 'Priya Patel',
        assignedTeam: 'Fire Station #7',
        createdAt: DateTime.now().subtract(const Duration(days: 1)),
        timeline: [
          {
            'status': 'reported',
            'time': DateTime.now()
                .subtract(const Duration(days: 1))
                .toIso8601String(),
            'note': 'Incident reported',
          },
          {
            'status': 'resolved',
            'time': DateTime.now()
                .subtract(const Duration(hours: 22))
                .toIso8601String(),
            'note': 'Fire contained and resolved',
          },
        ],
      ),
      IncidentModel(
        id: 'INC-003',
        title: 'Forest Fire - Ridge Road',
        description:
            'Brush fire spreading in the Northern Ridge forest area. Multiple hectares affected.',
        category: 'Forest',
        severity: 5,
        status: 'contained',
        latitude: 28.7041,
        longitude: 77.1025,
        address: 'Northern Ridge, New Delhi',
        reporterName: 'Amit Kumar',
        assignedTeam: 'Fire Station #3, #5',
        createdAt: DateTime.now().subtract(const Duration(hours: 6)),
        aiAnalysis: {
          'severity_score': 5,
          'risk_level': 'Critical',
          'fire_type': 'Wildfire',
          'spread_risk': 'High',
          'recommended_response': '4 fire engines, aerial support',
          'confidence': 0.92,
        },
      ),
    ];
  }
}
