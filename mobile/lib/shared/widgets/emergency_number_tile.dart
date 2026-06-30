import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import '../../core/theme/app_colors.dart';

class EmergencyNumberTile extends StatelessWidget {
  final String number;
  final String label;
  final IconData icon;
  final Color? color;

  const EmergencyNumberTile({
    super.key,
    required this.number,
    required this.label,
    required this.icon,
    this.color,
  });

  Future<void> _makeCall() async {
    final uri = Uri.parse('tel:$number');
    if (await canLaunchUrl(uri)) {
      await launchUrl(uri);
    }
  }

  @override
  Widget build(BuildContext context) {
    final tileColor = color ?? AppColors.fireOrange;
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return GestureDetector(
      onTap: _makeCall,
      child: Container(
        width: 100,
        padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 8),
        decoration: BoxDecoration(
          color: isDark
              ? tileColor.withValues(alpha: 0.15)
              : tileColor.withValues(alpha: 0.08),
          borderRadius: BorderRadius.circular(16),
          border: Border.all(
            color: tileColor.withValues(alpha: 0.3),
            width: 1,
          ),
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: tileColor.withValues(alpha: 0.2),
                shape: BoxShape.circle,
              ),
              child: Icon(icon, color: tileColor, size: 22),
            ),
            const SizedBox(height: 8),
            Text(
              number,
              style: TextStyle(
                color: tileColor,
                fontSize: 18,
                fontWeight: FontWeight.w800,
              ),
            ),
            const SizedBox(height: 2),
            Text(
              label,
              style: TextStyle(
                color: tileColor.withValues(alpha: 0.8),
                fontSize: 10,
                fontWeight: FontWeight.w600,
              ),
              textAlign: TextAlign.center,
              overflow: TextOverflow.ellipsis,
            ),
          ],
        ),
      ),
    );
  }

  static IconData iconForType(String type) {
    switch (type) {
      case 'fire':
        return Icons.local_fire_department;
      case 'emergency':
        return Icons.emergency;
      case 'ambulance':
        return Icons.local_hospital;
      case 'police':
        return Icons.local_police;
      default:
        return Icons.phone;
    }
  }

  static Color colorForType(String type) {
    switch (type) {
      case 'fire':
        return AppColors.fireDeepRed;
      case 'emergency':
        return AppColors.fireOrange;
      case 'ambulance':
        return AppColors.hospitalColor;
      case 'police':
        return AppColors.policeColor;
      default:
        return AppColors.fireOrange;
    }
  }
}
