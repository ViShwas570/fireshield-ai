import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:fireshield_ai/core/theme/app_theme.dart';
import 'package:fireshield_ai/shared/widgets/widgets.dart';
import 'package:fireshield_ai/shared/models/models.dart';

/// Main home screen with SOS button, quick actions, and emergency numbers
class HomeScreen extends StatelessWidget {
  final UserModel? user;
  final List<IncidentModel> recentIncidents;
  final VoidCallback onSOS;
  final VoidCallback onChat;
  final VoidCallback onMap;
  final VoidCallback onIncidents;
  final VoidCallback onProfile;

  const HomeScreen({
    super.key,
    this.user,
    this.recentIncidents = const [],
    required this.onSOS,
    required this.onChat,
    required this.onMap,
    required this.onIncidents,
    required this.onProfile,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Header
              Row(
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Hello, ${user?.name.split(' ').first ?? 'Citizen'} 👋',
                          style: GoogleFonts.outfit(
                              fontSize: 24, fontWeight: FontWeight.w700),
                        ),
                        const SizedBox(height: 4),
                        Text('Stay safe. We\'re here for you.',
                            style: TextStyle(
                                color: Theme.of(context)
                                    .colorScheme
                                    .onSurface
                                    .withOpacity(0.6))),
                      ],
                    ),
                  ),
                  GestureDetector(
                    onTap: onProfile,
                    child: CircleAvatar(
                      radius: 22,
                      backgroundColor: AppColors.primary.withOpacity(0.1),
                      child: Text(
                        user?.name.isNotEmpty == true
                            ? user!.name[0].toUpperCase()
                            : 'U',
                        style: const TextStyle(
                            color: AppColors.primary,
                            fontWeight: FontWeight.w700,
                            fontSize: 18),
                      ),
                    ),
                  ),
                ],
              ),

              const SizedBox(height: 28),

              // SOS Button
              Center(
                child: _SOSButton(onPressed: onSOS),
              ),

              const SizedBox(height: 28),

              // Quick Actions
              Text('Quick Actions',
                  style: GoogleFonts.outfit(
                      fontSize: 18, fontWeight: FontWeight.w700)),
              const SizedBox(height: 12),
              Row(
                children: [
                  Expanded(
                    child: _QuickActionCard(
                      icon: Icons.fire_extinguisher,
                      title: 'Report Fire',
                      color: AppColors.danger,
                      onTap: onSOS,
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: _QuickActionCard(
                      icon: Icons.chat_bubble_outline,
                      title: 'AI Chat',
                      color: AppColors.purple,
                      onTap: onChat,
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: _QuickActionCard(
                      icon: Icons.map_outlined,
                      title: 'Nearby',
                      color: AppColors.info,
                      onTap: onMap,
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: _QuickActionCard(
                      icon: Icons.history,
                      title: 'History',
                      color: AppColors.success,
                      onTap: onIncidents,
                    ),
                  ),
                ],
              ),

              const SizedBox(height: 28),

              // Emergency Numbers
              Text('Emergency Numbers',
                  style: GoogleFonts.outfit(
                      fontSize: 18, fontWeight: FontWeight.w700)),
              const SizedBox(height: 12),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  EmergencyNumberTile(
                    label: 'Fire',
                    number: '101',
                    icon: Icons.local_fire_department,
                    color: AppColors.danger,
                    onTap: () => _callNumber('101'),
                  ),
                  EmergencyNumberTile(
                    label: 'Emergency',
                    number: '112',
                    icon: Icons.emergency,
                    color: AppColors.primary,
                    onTap: () => _callNumber('112'),
                  ),
                  EmergencyNumberTile(
                    label: 'Ambulance',
                    number: '108',
                    icon: Icons.medical_services,
                    color: AppColors.success,
                    onTap: () => _callNumber('108'),
                  ),
                  EmergencyNumberTile(
                    label: 'Police',
                    number: '100',
                    icon: Icons.local_police,
                    color: AppColors.info,
                    onTap: () => _callNumber('100'),
                  ),
                ],
              ),

              const SizedBox(height: 28),

              // Safety Tips
              Text('Safety Tips',
                  style: GoogleFonts.outfit(
                      fontSize: 18, fontWeight: FontWeight.w700)),
              const SizedBox(height: 12),
              SizedBox(
                height: 120,
                child: ListView(
                  scrollDirection: Axis.horizontal,
                  children: const [
                    _SafetyTipCard(
                      tip: 'Install smoke detectors on every floor',
                      icon: Icons.sensors,
                      gradient: [Color(0xFFFF5722), Color(0xFFFF9800)],
                    ),
                    _SafetyTipCard(
                      tip: 'Keep fire extinguisher in kitchen',
                      icon: Icons.fire_extinguisher,
                      gradient: [Color(0xFF3B82F6), Color(0xFF8B5CF6)],
                    ),
                    _SafetyTipCard(
                      tip: 'Plan escape routes with family',
                      icon: Icons.route,
                      gradient: [Color(0xFF22C55E), Color(0xFF14B8A6)],
                    ),
                    _SafetyTipCard(
                      tip: 'Never leave cooking unattended',
                      icon: Icons.restaurant,
                      gradient: [Color(0xFFEAB308), Color(0xFFF97316)],
                    ),
                  ],
                ),
              ),

              // Recent Incidents
              if (recentIncidents.isNotEmpty) ...[
                const SizedBox(height: 28),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text('Recent Reports',
                        style: GoogleFonts.outfit(
                            fontSize: 18, fontWeight: FontWeight.w700)),
                    TextButton(
                        onPressed: onIncidents,
                        child: const Text('View All')),
                  ],
                ),
                const SizedBox(height: 8),
                ...recentIncidents.take(3).map((inc) => _IncidentTile(
                      incident: inc,
                      onTap: onIncidents,
                    )),
              ],

              const SizedBox(height: 20),
            ],
          ),
        ),
      ),
    );
  }

  void _callNumber(String number) async {
    final uri = Uri.parse('tel:$number');
    if (await canLaunchUrl(uri)) {
      await launchUrl(uri);
    }
  }
}

/// Pulsating SOS Button
class _SOSButton extends StatefulWidget {
  final VoidCallback onPressed;
  const _SOSButton({required this.onPressed});

  @override
  State<_SOSButton> createState() => _SOSButtonState();
}

class _SOSButtonState extends State<_SOSButton>
    with SingleTickerProviderStateMixin {
  late AnimationController _animController;

  @override
  void initState() {
    super.initState();
    _animController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1500),
    )..repeat(reverse: true);
  }

  @override
  void dispose() {
    _animController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _animController,
      builder: (context, child) {
        final scale = 1.0 + (_animController.value * 0.08);
        return Transform.scale(
          scale: scale,
          child: GestureDetector(
            onTap: () {
              HapticFeedback.heavyImpact();
              widget.onPressed();
            },
            child: Container(
              width: 140,
              height: 140,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                gradient: AppColors.fireGradient,
                boxShadow: [
                  BoxShadow(
                    color: AppColors.primary.withOpacity(0.4 + _animController.value * 0.2),
                    blurRadius: 30 + _animController.value * 20,
                    spreadRadius: 5,
                  ),
                ],
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.emergency, color: Colors.white, size: 40),
                  const SizedBox(height: 4),
                  Text('SOS',
                      style: GoogleFonts.outfit(
                          color: Colors.white,
                          fontSize: 24,
                          fontWeight: FontWeight.w900)),
                ],
              ),
            ),
          ),
        );
      },
    );
  }
}

/// Quick action card
class _QuickActionCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final Color color;
  final VoidCallback onTap;

  const _QuickActionCard({
    required this.icon,
    required this.title,
    required this.color,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 16),
        decoration: BoxDecoration(
          color: color.withOpacity(0.08),
          borderRadius: BorderRadius.circular(14),
          border: Border.all(color: color.withOpacity(0.15)),
        ),
        child: Column(
          children: [
            Icon(icon, color: color, size: 28),
            const SizedBox(height: 8),
            Text(title,
                style: TextStyle(
                    fontSize: 11,
                    fontWeight: FontWeight.w600,
                    color: color)),
          ],
        ),
      ),
    );
  }
}

/// Safety tip card
class _SafetyTipCard extends StatelessWidget {
  final String tip;
  final IconData icon;
  final List<Color> gradient;

  const _SafetyTipCard({
    required this.tip,
    required this.icon,
    required this.gradient,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 200,
      margin: const EdgeInsets.only(right: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        gradient: LinearGradient(colors: gradient),
        borderRadius: BorderRadius.circular(16),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(icon, color: Colors.white, size: 28),
          const SizedBox(height: 10),
          Text(tip,
              style: const TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.w600,
                  fontSize: 13)),
        ],
      ),
    );
  }
}

/// Incident list tile
class _IncidentTile extends StatelessWidget {
  final IncidentModel incident;
  final VoidCallback onTap;

  const _IncidentTile({required this.incident, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        onTap: onTap,
        leading: SeverityBadge(severity: incident.severity),
        title: Text(incident.title,
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
            style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14)),
        subtitle: Text('📍 ${incident.address}',
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
            style: const TextStyle(fontSize: 12)),
        trailing: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.end,
          children: [
            StatusBadge(status: incident.status),
            const SizedBox(height: 4),
            Text(incident.timeAgo,
                style: TextStyle(
                    fontSize: 11,
                    color: Theme.of(context)
                        .colorScheme
                        .onSurface
                        .withOpacity(0.5))),
          ],
        ),
      ),
    );
  }
}
