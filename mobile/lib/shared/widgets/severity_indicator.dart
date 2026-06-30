import 'package:flutter/material.dart';
import '../../core/theme/app_colors.dart';

class SeverityIndicator extends StatelessWidget {
  final int severity;
  final double size;
  final bool showLabel;
  final bool animate;

  const SeverityIndicator({
    super.key,
    required this.severity,
    this.size = 48,
    this.showLabel = true,
    this.animate = true,
  });

  @override
  Widget build(BuildContext context) {
    final color = AppColors.severityColor(severity);
    final label = AppColors.severityLabel(severity);
    final progress = severity / 5.0;

    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        SizedBox(
          width: size,
          height: size,
          child: Stack(
            alignment: Alignment.center,
            children: [
              SizedBox(
                width: size,
                height: size,
                child: TweenAnimationBuilder<double>(
                  tween: Tween(begin: 0, end: progress),
                  duration: animate
                      ? const Duration(milliseconds: 1200)
                      : Duration.zero,
                  curve: Curves.easeOutCubic,
                  builder: (context, value, _) {
                    return CircularProgressIndicator(
                      value: value,
                      strokeWidth: 4,
                      backgroundColor: color.withValues(alpha: 0.15),
                      valueColor: AlwaysStoppedAnimation(color),
                      strokeCap: StrokeCap.round,
                    );
                  },
                ),
              ),
              Container(
                width: size * 0.7,
                height: size * 0.7,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: color.withValues(alpha: 0.15),
                ),
                child: Center(
                  child: Text(
                    '$severity',
                    style: TextStyle(
                      color: color,
                      fontSize: size * 0.3,
                      fontWeight: FontWeight.w800,
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
        if (showLabel) ...[
          const SizedBox(height: 4),
          Text(
            label,
            style: TextStyle(
              color: color,
              fontSize: 11,
              fontWeight: FontWeight.w600,
            ),
          ),
        ],
      ],
    );
  }
}
