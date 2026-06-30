class ChatMessageModel {
  final String id;
  final String text;
  final bool isUser;
  final DateTime timestamp;
  final List<String>? suggestions;
  final Map<String, dynamic>? metadata;

  const ChatMessageModel({
    required this.id,
    required this.text,
    required this.isUser,
    required this.timestamp,
    this.suggestions,
    this.metadata,
  });

  factory ChatMessageModel.fromJson(Map<String, dynamic> json) {
    return ChatMessageModel(
      id: json['id']?.toString() ?? DateTime.now().millisecondsSinceEpoch.toString(),
      text: json['text']?.toString() ?? json['message']?.toString() ?? '',
      isUser: json['is_user'] == true || json['role'] == 'user',
      timestamp: DateTime.tryParse(json['timestamp']?.toString() ?? '') ?? DateTime.now(),
      suggestions: (json['suggestions'] as List?)?.map((e) => e.toString()).toList(),
      metadata: json['metadata'] as Map<String, dynamic>?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'text': text,
      'is_user': isUser,
      'timestamp': timestamp.toIso8601String(),
      'suggestions': suggestions,
      'metadata': metadata,
    };
  }

  factory ChatMessageModel.user(String text) {
    return ChatMessageModel(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      text: text,
      isUser: true,
      timestamp: DateTime.now(),
    );
  }

  factory ChatMessageModel.bot(String text, {List<String>? suggestions}) {
    return ChatMessageModel(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      text: text,
      isUser: false,
      timestamp: DateTime.now(),
      suggestions: suggestions,
    );
  }

  factory ChatMessageModel.greeting() {
    return ChatMessageModel(
      id: 'greeting',
      text:
          '🔥 Welcome to FireShield AI!\n\nI\'m your AI fire safety assistant. I can help you with:\n\n'
          '• Report a fire emergency\n'
          '• Fire safety guidelines\n'
          '• Find nearby fire stations\n'
          '• First aid for burns\n'
          '• Emergency evacuation tips\n\n'
          'How can I help you today?',
      isUser: false,
      timestamp: DateTime.now(),
      suggestions: [
        'Report a fire',
        'Safety tips',
        'Nearby fire stations',
        'First aid for burns',
        'Emergency numbers',
      ],
    );
  }
}
