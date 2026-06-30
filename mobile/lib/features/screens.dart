import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:fireshield_ai/core/theme/app_theme.dart';
import 'package:fireshield_ai/shared/widgets/widgets.dart';

/// SOS Emergency Reporting Screen
class SOSScreen extends StatefulWidget {
  final Future<Map<String, dynamic>?> Function(String description, String category) onSubmitSOS;
  const SOSScreen({super.key, required this.onSubmitSOS});

  @override
  State<SOSScreen> createState() => _SOSScreenState();
}

class _SOSScreenState extends State<SOSScreen> {
  final _descController = TextEditingController();
  String _category = 'building';
  bool _isSubmitting = false;
  bool _isAnalyzing = false;
  Map<String, dynamic>? _result;

  final _categories = {
    'building': '🏢 Building',
    'industrial': '🏭 Industrial',
    'forest': '🌲 Forest',
    'vehicle': '🚗 Vehicle',
    'kitchen': '🍳 Kitchen',
    'electrical': '⚡ Electrical',
    'gas_leak': '💨 Gas Leak',
    'other': '🔥 Other',
  };

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Row(
          children: [
            Container(
              width: 8, height: 8,
              decoration: const BoxDecoration(
                color: AppColors.danger,
                shape: BoxShape.circle,
              ),
            ),
            const SizedBox(width: 8),
            const Text('Emergency Report'),
          ],
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Location info
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: AppColors.info.withOpacity(0.08),
                borderRadius: BorderRadius.circular(14),
                border: Border.all(color: AppColors.info.withOpacity(0.2)),
              ),
              child: const Row(
                children: [
                  Icon(Icons.location_on, color: AppColors.info),
                  SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('📍 GPS Location Captured',
                            style: TextStyle(fontWeight: FontWeight.w600, fontSize: 14)),
                        Text('Current location will be shared with responders',
                            style: TextStyle(fontSize: 12, color: Colors.grey)),
                      ],
                    ),
                  ),
                  Icon(Icons.check_circle, color: AppColors.success),
                ],
              ),
            ),

            const SizedBox(height: 20),

            // Category selection
            Text('Fire Category',
                style: GoogleFonts.outfit(
                    fontSize: 16, fontWeight: FontWeight.w700)),
            const SizedBox(height: 10),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: _categories.entries.map((e) {
                final selected = _category == e.key;
                return ChoiceChip(
                  label: Text(e.value),
                  selected: selected,
                  onSelected: (_) => setState(() => _category = e.key),
                  selectedColor: AppColors.primary.withOpacity(0.2),
                  labelStyle: TextStyle(
                    color: selected ? AppColors.primary : null,
                    fontWeight: selected ? FontWeight.w600 : FontWeight.w400,
                  ),
                );
              }).toList(),
            ),

            const SizedBox(height: 20),

            // Description
            Text('Description',
                style: GoogleFonts.outfit(
                    fontSize: 16, fontWeight: FontWeight.w700)),
            const SizedBox(height: 10),
            TextField(
              controller: _descController,
              maxLines: 4,
              decoration: const InputDecoration(
                hintText: 'Describe the emergency situation...\n(e.g., Fire on 3rd floor, people trapped)',
              ),
            ),

            const SizedBox(height: 24),

            // Submit SOS
            GradientButton(
              text: _isSubmitting ? 'Sending SOS...' : '🚨 SEND SOS ALERT',
              icon: Icons.emergency,
              isLoading: _isSubmitting,
              onPressed: _submitSOS,
            ),

            // Result
            if (_result != null) ...[
              const SizedBox(height: 24),
              Container(
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  color: AppColors.success.withOpacity(0.08),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: AppColors.success.withOpacity(0.3)),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        const Icon(Icons.check_circle,
                            color: AppColors.success, size: 28),
                        const SizedBox(width: 10),
                        Text('SOS Alert Sent!',
                            style: GoogleFonts.outfit(
                                fontSize: 18,
                                fontWeight: FontWeight.w700,
                                color: AppColors.success)),
                      ],
                    ),
                    const SizedBox(height: 12),
                    Text('Incident ID: ${_result!['incident_id'] ?? 'N/A'}',
                        style: const TextStyle(fontWeight: FontWeight.w600)),
                    if (_result!['ai_analysis'] != null) ...[
                      const SizedBox(height: 8),
                      Text(
                          'AI Severity: ${_result!['ai_analysis']['severity_score']}/5.0',
                          style: const TextStyle(fontWeight: FontWeight.w600)),
                      Text(
                          'Risk Level: ${_result!['ai_analysis']['risk_level']}'),
                      Text(
                          'Recommended Units: ${_result!['ai_analysis']['recommended_units']}'),
                    ],
                    if (_result!['nearest_station'] != null) ...[
                      const SizedBox(height: 8),
                      Text(
                          '🚒 Nearest: ${_result!['nearest_station']['name']}'),
                      Text(
                          '📏 Distance: ${_result!['nearest_station']['distance_km']} km'),
                    ],
                    const SizedBox(height: 8),
                    Text(_result!['message'] ?? '',
                        style: const TextStyle(fontWeight: FontWeight.w600)),
                  ],
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }

  void _submitSOS() async {
    if (_descController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please describe the emergency')),
      );
      return;
    }
    setState(() => _isSubmitting = true);
    try {
      final result = await widget.onSubmitSOS(_descController.text, _category);
      setState(() => _result = result);
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $e'), backgroundColor: AppColors.danger),
        );
      }
    } finally {
      if (mounted) setState(() => _isSubmitting = false);
    }
  }
}

/// AI Chatbot Screen
class ChatbotScreen extends StatefulWidget {
  final Future<Map<String, dynamic>> Function(String message, String lang) onSendMessage;
  const ChatbotScreen({super.key, required this.onSendMessage});

  @override
  State<ChatbotScreen> createState() => _ChatbotScreenState();
}

class _ChatbotScreenState extends State<ChatbotScreen> {
  final _msgController = TextEditingController();
  final _scrollController = ScrollController();
  final List<_ChatMsg> _messages = [];
  bool _isTyping = false;
  String _lang = 'en';

  @override
  void initState() {
    super.initState();
    _messages.add(_ChatMsg(
      text: '🔥 **FireShield AI Emergency Assistant**\n\n'
          'I can help you with fire emergencies:\n'
          '• Evacuation procedures\n'
          '• First aid for burns\n'
          '• Smoke inhalation treatment\n'
          '• Electrical fire safety\n\n'
          '📞 Emergency: 101 (Fire) | 112 (All)',
      isUser: false,
      suggestions: ['Evacuation guide', 'First aid for burns', "I'm trapped", 'Electrical fire'],
    ));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Row(
          children: [
            Container(
              width: 36, height: 36,
              decoration: BoxDecoration(
                gradient: AppColors.fireGradient,
                borderRadius: BorderRadius.circular(10),
              ),
              child: const Icon(Icons.smart_toy, color: Colors.white, size: 20),
            ),
            const SizedBox(width: 10),
            const Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('AI Emergency Chat', style: TextStyle(fontSize: 16)),
                Text('Online • Ready to help',
                    style: TextStyle(fontSize: 11, color: Colors.grey)),
              ],
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => setState(() => _lang = _lang == 'en' ? 'hi' : 'en'),
            child: Text(_lang == 'en' ? 'हिंदी' : 'English',
                style: const TextStyle(fontWeight: FontWeight.w600)),
          ),
        ],
      ),
      body: Column(
        children: [
          // Messages
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              padding: const EdgeInsets.all(16),
              itemCount: _messages.length + (_isTyping ? 1 : 0),
              itemBuilder: (context, index) {
                if (_isTyping && index == _messages.length) {
                  return _TypingIndicator();
                }
                final msg = _messages[index];
                return _ChatBubble(
                  text: msg.text,
                  isUser: msg.isUser,
                  suggestions: msg.suggestions,
                  onSuggestionTap: _sendMessage,
                );
              },
            ),
          ),
          // Input
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.surface,
              border: Border(
                top: BorderSide(color: Colors.grey.withOpacity(0.2)),
              ),
            ),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _msgController,
                    decoration: InputDecoration(
                      hintText: _lang == 'en' ? 'Ask about fire safety...' : 'आग सुरक्षा के बारे में पूछें...',
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(24),
                        borderSide: BorderSide.none,
                      ),
                      contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                    ),
                    onSubmitted: (text) => _sendMessage(text),
                  ),
                ),
                const SizedBox(width: 8),
                Container(
                  decoration: const BoxDecoration(
                    gradient: AppColors.fireGradient,
                    shape: BoxShape.circle,
                  ),
                  child: IconButton(
                    icon: const Icon(Icons.send, color: Colors.white, size: 20),
                    onPressed: () => _sendMessage(_msgController.text),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  void _sendMessage(String text) async {
    if (text.trim().isEmpty) return;
    setState(() {
      _messages.add(_ChatMsg(text: text, isUser: true));
      _isTyping = true;
      _msgController.clear();
    });
    _scrollToBottom();

    try {
      final response = await widget.onSendMessage(text, _lang);
      setState(() {
        _isTyping = false;
        _messages.add(_ChatMsg(
          text: response['response'] ?? 'Sorry, I could not process that.',
          isUser: false,
          suggestions: List<String>.from(response['suggestions'] ?? []),
        ));
      });
    } catch (e) {
      setState(() {
        _isTyping = false;
        _messages.add(_ChatMsg(
          text: 'Connection error. In an emergency, call 101 (Fire) or 112.',
          isUser: false,
          suggestions: ['Try again', 'Call 101'],
        ));
      });
    }
    _scrollToBottom();
  }

  void _scrollToBottom() {
    Future.delayed(const Duration(milliseconds: 100), () {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }
}

class _ChatMsg {
  final String text;
  final bool isUser;
  final List<String> suggestions;
  _ChatMsg({required this.text, required this.isUser, this.suggestions = const []});
}

class _ChatBubble extends StatelessWidget {
  final String text;
  final bool isUser;
  final List<String> suggestions;
  final Function(String) onSuggestionTap;

  const _ChatBubble({
    required this.text,
    required this.isUser,
    this.suggestions = const [],
    required this.onSuggestionTap,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Column(
        crossAxisAlignment:
            isUser ? CrossAxisAlignment.end : CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment:
                isUser ? MainAxisAlignment.end : MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              if (!isUser)
                Container(
                  width: 30, height: 30,
                  margin: const EdgeInsets.only(right: 8, top: 4),
                  decoration: BoxDecoration(
                    gradient: AppColors.fireGradient,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: const Icon(Icons.smart_toy, color: Colors.white, size: 16),
                ),
              Flexible(
                child: Container(
                  padding: const EdgeInsets.all(14),
                  decoration: BoxDecoration(
                    color: isUser
                        ? AppColors.primary
                        : Theme.of(context).brightness == Brightness.dark
                            ? AppColors.darkCard
                            : Colors.grey.shade100,
                    borderRadius: BorderRadius.only(
                      topLeft: const Radius.circular(16),
                      topRight: const Radius.circular(16),
                      bottomLeft: Radius.circular(isUser ? 16 : 4),
                      bottomRight: Radius.circular(isUser ? 4 : 16),
                    ),
                  ),
                  child: Text(
                    text,
                    style: TextStyle(
                      color: isUser ? Colors.white : null,
                      fontSize: 14,
                      height: 1.5,
                    ),
                  ),
                ),
              ),
            ],
          ),
          if (suggestions.isNotEmpty && !isUser) ...[
            const SizedBox(height: 8),
            Wrap(
              spacing: 6,
              runSpacing: 6,
              children: suggestions.map((s) => ActionChip(
                    label: Text(s, style: const TextStyle(fontSize: 12)),
                    onPressed: () => onSuggestionTap(s),
                    backgroundColor: AppColors.primary.withOpacity(0.08),
                    side: BorderSide(color: AppColors.primary.withOpacity(0.2)),
                  )).toList(),
            ),
          ],
        ],
      ),
    );
  }
}

class _TypingIndicator extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Row(
        children: [
          Container(
            width: 30, height: 30,
            margin: const EdgeInsets.only(right: 8),
            decoration: BoxDecoration(
              gradient: AppColors.fireGradient,
              borderRadius: BorderRadius.circular(8),
            ),
            child: const Icon(Icons.smart_toy, color: Colors.white, size: 16),
          ),
          Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              color: Theme.of(context).brightness == Brightness.dark
                  ? AppColors.darkCard
                  : Colors.grey.shade100,
              borderRadius: BorderRadius.circular(16),
            ),
            child: const Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                _Dot(delay: 0),
                SizedBox(width: 4),
                _Dot(delay: 200),
                SizedBox(width: 4),
                _Dot(delay: 400),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _Dot extends StatefulWidget {
  final int delay;
  const _Dot({required this.delay});

  @override
  State<_Dot> createState() => _DotState();
}

class _DotState extends State<_Dot> with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 600),
    );
    Future.delayed(Duration(milliseconds: widget.delay), () {
      if (mounted) _controller.repeat(reverse: true);
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        return Container(
          width: 8,
          height: 8,
          decoration: BoxDecoration(
            color: Colors.grey.withOpacity(0.3 + _controller.value * 0.7),
            shape: BoxShape.circle,
          ),
        );
      },
    );
  }
}

/// Incidents List Screen
class IncidentsListScreen extends StatelessWidget {
  final List<IncidentModel> incidents;
  final Function(IncidentModel) onTap;

  const IncidentsListScreen({
    super.key,
    required this.incidents,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Incident History')),
      body: incidents.isEmpty
          ? Center(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Icon(Icons.check_circle_outline,
                      size: 64, color: Colors.grey.shade400),
                  const SizedBox(height: 16),
                  Text('No incidents reported',
                      style: TextStyle(
                          fontSize: 16, color: Colors.grey.shade500)),
                ],
              ),
            )
          : ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: incidents.length,
              itemBuilder: (context, index) {
                final inc = incidents[index];
                return Card(
                  margin: const EdgeInsets.only(bottom: 10),
                  child: ListTile(
                    onTap: () => onTap(inc),
                    leading: SeverityBadge(severity: inc.severity, size: 40),
                    title: Text(inc.title,
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                        style: const TextStyle(
                            fontWeight: FontWeight.w600, fontSize: 14)),
                    subtitle: Padding(
                      padding: const EdgeInsets.only(top: 6),
                      child: Row(
                        children: [
                          const Icon(Icons.location_on,
                              size: 13, color: Colors.grey),
                          const SizedBox(width: 4),
                          Expanded(
                            child: Text(inc.address,
                                maxLines: 1,
                                overflow: TextOverflow.ellipsis,
                                style: const TextStyle(fontSize: 12)),
                          ),
                        ],
                      ),
                    ),
                    trailing: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      crossAxisAlignment: CrossAxisAlignment.end,
                      children: [
                        StatusBadge(status: inc.status),
                        const SizedBox(height: 4),
                        Text(inc.timeAgo,
                            style: const TextStyle(
                                fontSize: 11, color: Colors.grey)),
                      ],
                    ),
                  ),
                );
              },
            ),
    );
  }
}

/// Nearby Services Screen (without Google Maps — list-based)
class NearbyServicesScreen extends StatefulWidget {
  final Future<List<NearbyServiceModel>> Function(String type) fetchNearby;
  const NearbyServicesScreen({super.key, required this.fetchNearby});

  @override
  State<NearbyServicesScreen> createState() => _NearbyServicesScreenState();
}

class _NearbyServicesScreenState extends State<NearbyServicesScreen>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;
  List<NearbyServiceModel> _services = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
    _tabController.addListener(() => _loadServices());
    _loadServices();
  }

  void _loadServices() async {
    setState(() => _loading = true);
    final types = ['fire_station', 'hospital', 'police'];
    try {
      _services = await widget.fetchNearby(types[_tabController.index]);
    } catch (_) {
      _services = [];
    }
    if (mounted) setState(() => _loading = false);
  }

  @override
  Widget build(BuildContext context) {
    final icons = [Icons.local_fire_department, Icons.local_hospital, Icons.local_police];
    final colors = [AppColors.danger, AppColors.success, AppColors.info];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Nearby Services'),
        bottom: TabBar(
          controller: _tabController,
          tabs: const [
            Tab(icon: Icon(Icons.local_fire_department), text: 'Fire'),
            Tab(icon: Icon(Icons.local_hospital), text: 'Hospital'),
            Tab(icon: Icon(Icons.local_police), text: 'Police'),
          ],
        ),
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : _services.isEmpty
              ? const Center(child: Text('No nearby services found'))
              : ListView.builder(
                  padding: const EdgeInsets.all(16),
                  itemCount: _services.length,
                  itemBuilder: (context, index) {
                    final s = _services[index];
                    return Card(
                      margin: const EdgeInsets.only(bottom: 10),
                      child: ListTile(
                        leading: CircleAvatar(
                          backgroundColor: colors[_tabController.index].withOpacity(0.1),
                          child: Icon(icons[_tabController.index],
                              color: colors[_tabController.index]),
                        ),
                        title: Text(s.name,
                            style: const TextStyle(fontWeight: FontWeight.w600)),
                        subtitle: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('📍 ${s.address}',
                                style: const TextStyle(fontSize: 12)),
                            Text('📏 ${s.distanceKm} km away',
                                style: TextStyle(
                                    fontSize: 12,
                                    color: colors[_tabController.index],
                                    fontWeight: FontWeight.w600)),
                          ],
                        ),
                        trailing: IconButton(
                          icon: const Icon(Icons.phone, color: AppColors.success),
                          onPressed: () async {
                            final uri = Uri.parse('tel:${s.phone}');
                            if (await canLaunchUrl(uri)) await launchUrl(uri);
                          },
                        ),
                      ),
                    );
                  },
                ),
    );
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }
}

/// Profile Screen
class ProfileScreen extends StatelessWidget {
  final UserModel? user;
  final int totalReports;
  final VoidCallback onLogout;
  final VoidCallback onSettings;

  const ProfileScreen({
    super.key,
    this.user,
    this.totalReports = 0,
    required this.onLogout,
    required this.onSettings,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Profile')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            // Avatar
            CircleAvatar(
              radius: 48,
              backgroundColor: AppColors.primary.withOpacity(0.1),
              child: Text(
                user?.name.isNotEmpty == true ? user!.name[0].toUpperCase() : 'U',
                style: GoogleFonts.outfit(
                    fontSize: 36,
                    fontWeight: FontWeight.w800,
                    color: AppColors.primary),
              ),
            ),
            const SizedBox(height: 16),
            Text(user?.name ?? 'User',
                style: GoogleFonts.outfit(
                    fontSize: 22, fontWeight: FontWeight.w700)),
            Text(user?.email ?? '',
                style: TextStyle(color: Colors.grey.shade500)),
            if (user?.phone.isNotEmpty == true)
              Text(user!.phone,
                  style: TextStyle(color: Colors.grey.shade500)),

            const SizedBox(height: 24),

            // Stats
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                _StatItem(value: '$totalReports', label: 'Reports'),
                _StatItem(
                    value: user?.role.toUpperCase() ?? 'CITIZEN',
                    label: 'Role'),
              ],
            ),

            const SizedBox(height: 32),

            // Menu items
            _MenuItem(
              icon: Icons.settings,
              title: 'Settings',
              subtitle: 'Theme, language, notifications',
              onTap: onSettings,
            ),
            _MenuItem(
              icon: Icons.info_outline,
              title: 'About FireShield AI',
              subtitle: 'Version 1.0.0',
              onTap: () {},
            ),
            _MenuItem(
              icon: Icons.logout,
              title: 'Logout',
              subtitle: 'Sign out of your account',
              onTap: onLogout,
              isDestructive: true,
            ),
          ],
        ),
      ),
    );
  }
}

class _StatItem extends StatelessWidget {
  final String value;
  final String label;
  const _StatItem({required this.value, required this.label});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(value,
            style: GoogleFonts.outfit(
                fontSize: 24,
                fontWeight: FontWeight.w800,
                color: AppColors.primary)),
        Text(label,
            style: TextStyle(fontSize: 12, color: Colors.grey.shade500)),
      ],
    );
  }
}

class _MenuItem extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final VoidCallback onTap;
  final bool isDestructive;

  const _MenuItem({
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.onTap,
    this.isDestructive = false,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        onTap: onTap,
        leading: Icon(icon,
            color: isDestructive ? AppColors.danger : AppColors.primary),
        title: Text(title,
            style: TextStyle(
                fontWeight: FontWeight.w600,
                color: isDestructive ? AppColors.danger : null)),
        subtitle: Text(subtitle, style: const TextStyle(fontSize: 12)),
        trailing: const Icon(Icons.chevron_right),
      ),
    );
  }
}

/// Settings Screen
class SettingsScreen extends StatefulWidget {
  final bool isDarkMode;
  final ValueChanged<bool> onThemeChanged;

  const SettingsScreen({
    super.key,
    required this.isDarkMode,
    required this.onThemeChanged,
  });

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  late bool _isDark;
  String _lang = 'English';

  @override
  void initState() {
    super.initState();
    _isDark = widget.isDarkMode;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Settings')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(
            child: SwitchListTile(
              title: const Text('Dark Mode',
                  style: TextStyle(fontWeight: FontWeight.w600)),
              subtitle: const Text('Toggle dark/light theme'),
              secondary: Icon(_isDark ? Icons.dark_mode : Icons.light_mode,
                  color: AppColors.primary),
              value: _isDark,
              onChanged: (val) {
                setState(() => _isDark = val);
                widget.onThemeChanged(val);
              },
            ),
          ),
          const SizedBox(height: 8),
          Card(
            child: ListTile(
              leading: const Icon(Icons.language, color: AppColors.primary),
              title: const Text('Language',
                  style: TextStyle(fontWeight: FontWeight.w600)),
              trailing: DropdownButton<String>(
                value: _lang,
                items: const [
                  DropdownMenuItem(value: 'English', child: Text('English')),
                  DropdownMenuItem(value: 'हिंदी', child: Text('हिंदी')),
                ],
                onChanged: (v) => setState(() => _lang = v!),
              ),
            ),
          ),
          const SizedBox(height: 8),
          Card(
            child: SwitchListTile(
              title: const Text('Push Notifications',
                  style: TextStyle(fontWeight: FontWeight.w600)),
              subtitle: const Text('Receive emergency alerts'),
              secondary:
                  const Icon(Icons.notifications, color: AppColors.primary),
              value: true,
              onChanged: (val) {},
            ),
          ),
        ],
      ),
    );
  }
}

// Need these imports for NearbyServiceModel
import 'package:fireshield_ai/shared/models/models.dart';
import 'package:url_launcher/url_launcher.dart';
