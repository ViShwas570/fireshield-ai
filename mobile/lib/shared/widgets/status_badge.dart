import 'package:flutter/material.dart';
import '../../core/theme/app_colors.dart';

class StatusBadge extends StatelessWidget {
  final String status;
  final double? fontSize;
  final EdgeInsetsGeometry? padding;

  const StatusBadge({
    super.key,
    required this.status,
    this.fontSize,
    this.padding,
  });

  String get _displayText {
    switch (status.toLowerCase()) {
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

  IconData get _icon {
    switch (status.toLowerCase()) {
      case 'reported':
        return Icons.report_outlined;
      case 'verified':
        return Icons.verified_outlined;
      case 'responding':
        return Icons.local_fire_department;
      case 'contained':
        return Icons.shield_outlined;
      case 'resolved':
        return Icons.check_circle_outline;
      case 'false_alarm':
        return Icons.info_outline;
      default:
        return Icons.circle_outlined;
    }
  }

  @override
  Widget build(BuildContext context) {
    final color = AppColors.statusColor(status);

    return TweenAnimationBuilder<double>(
      tween: Tween(begin: 0.0, end: 1.0),
      duration: const Duration(milliseconds: 600),
      curve: Curves.elasticOut,
      builder: (context, value, child) {
        return Transform.scale(
          scale: value,
          child: child,
        );
      },
      child: Container(
        padding: padding ??
            const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
        decoration: BoxDecoration(
          color: color.withValues(alpha: 0.15),
          borderRadius: BorderRadius.circular(20),
          border: Border.all(
            color: color.withValues(alpha: 0.3),
            width: 1,
          ),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(_icon, color: color, size: (fontSize ?? 12) + 2),
            const SizedBox(width: 4),
            Text(
              _displayText,
              style: TextStyle(
                color: color,
                fontSize: fontSize ?? 12,
                fontWeight: FontWeight.w700,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
