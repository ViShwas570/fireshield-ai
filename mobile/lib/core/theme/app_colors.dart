import 'dart:ui';

import 'package:flutter/material.dart';

class AppColors {
  AppColors._();

  // Primary Fire Colors
  static const Color fireOrange = Color(0xFFFF5722);
  static const Color fireAmber = Color(0xFFFFC107);
  static const Color fireDeepRed = Color(0xFFD32F2F);
  static const Color fireYellow = Color(0xFFFFEB3B);
  static const Color fireDarkRed = Color(0xFFB71C1C);
  static const Color emberGlow = Color(0xFFFF8A65);
  static const Color ashGray = Color(0xFF9E9E9E);

  // Severity Colors (1=Low to 5=Critical)
  static const Color severity1 = Color(0xFF4CAF50);
  static const Color severity2 = Color(0xFF8BC34A);
  static const Color severity3 = Color(0xFFFFC107);
  static const Color severity4 = Color(0xFFFF9800);
  static const Color severity5 = Color(0xFFF44336);

  static Color severityColor(int severity) {
    switch (severity.clamp(1, 5)) {
      case 1:
        return severity1;
      case 2:
        return severity2;
      case 3:
        return severity3;
      case 4:
        return severity4;
      case 5:
        return severity5;
      default:
        return severity3;
    }
  }

  static String severityLabel(int severity) {
    switch (severity.clamp(1, 5)) {
      case 1:
        return 'Low';
      case 2:
        return 'Moderate';
      case 3:
        return 'High';
      case 4:
        return 'Severe';
      case 5:
        return 'Critical';
      default:
        return 'Unknown';
    }
  }

  // Status Colors
  static const Color statusReported = Color(0xFFFF9800);
  static const Color statusVerified = Color(0xFF2196F3);
  static const Color statusResponding = Color(0xFFFF5722);
  static const Color statusContained = Color(0xFF9C27B0);
  static const Color statusResolved = Color(0xFF4CAF50);
  static const Color statusFalseAlarm = Color(0xFF9E9E9E);

  static Color statusColor(String status) {
    switch (status.toLowerCase()) {
      case 'reported':
        return statusReported;
      case 'verified':
        return statusVerified;
      case 'responding':
        return statusResponding;
      case 'contained':
        return statusContained;
      case 'resolved':
        return statusResolved;
      case 'false_alarm':
        return statusFalseAlarm;
      default:
        return statusReported;
    }
  }

  // Service Type Colors
  static const Color fireStationColor = Color(0xFFE53935);
  static const Color hospitalColor = Color(0xFF1E88E5);
  static const Color policeColor = Color(0xFF43A047);

  // Gradients
  static const LinearGradient fireGradient = LinearGradient(
    colors: [fireDeepRed, fireOrange, fireAmber],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  static const LinearGradient fireGradientVertical = LinearGradient(
    colors: [fireDarkRed, fireDeepRed, fireOrange],
    begin: Alignment.topCenter,
    end: Alignment.bottomCenter,
  );

  static const LinearGradient warmGradient = LinearGradient(
    colors: [Color(0xFFFF8A65), Color(0xFFFF5722), Color(0xFFD32F2F)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  static const LinearGradient darkGradient = LinearGradient(
    colors: [Color(0xFF1A1A2E), Color(0xFF16213E), Color(0xFF0F3460)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  static const LinearGradient darkSurfaceGradient = LinearGradient(
    colors: [Color(0xFF1E1E2E), Color(0xFF2D2D3F)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  static const LinearGradient sosGradient = LinearGradient(
    colors: [Color(0xFFFF1744), Color(0xFFD50000)],
    begin: Alignment.topCenter,
    end: Alignment.bottomCenter,
  );

  // Glass Effect Colors
  static Color glassWhite = Colors.white.withValues(alpha: 0.1);
  static Color glassBorder = Colors.white.withValues(alpha: 0.2);
  static Color glassDark = Colors.black.withValues(alpha: 0.2);

  // Dark Mode Surfaces
  static const Color darkBackground = Color(0xFF0D1117);
  static const Color darkSurface = Color(0xFF161B22);
  static const Color darkCard = Color(0xFF21262D);
  static const Color darkElevated = Color(0xFF30363D);

  // Light Mode Surfaces
  static const Color lightBackground = Color(0xFFFAFAFA);
  static const Color lightSurface = Color(0xFFFFFFFF);
  static const Color lightCard = Color(0xFFFFFFFF);
}
