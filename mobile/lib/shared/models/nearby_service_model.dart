class NearbyServiceModel {
  final String id;
  final String name;
  final String type;
  final double latitude;
  final double longitude;
  final String address;
  final String? phone;
  final double? distance;

  const NearbyServiceModel({
    required this.id,
    required this.name,
    required this.type,
    required this.latitude,
    required this.longitude,
    required this.address,
    this.phone,
    this.distance,
  });

  factory NearbyServiceModel.fromJson(Map<String, dynamic> json) {
    return NearbyServiceModel(
      id: json['id']?.toString() ?? '',
      name: json['name']?.toString() ?? '',
      type: json['type']?.toString() ?? 'fire_station',
      latitude: double.tryParse(json['latitude']?.toString() ?? '0') ?? 0.0,
      longitude: double.tryParse(json['longitude']?.toString() ?? '0') ?? 0.0,
      address: json['address']?.toString() ?? '',
      phone: json['phone']?.toString(),
      distance: double.tryParse(json['distance']?.toString() ?? ''),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'type': type,
      'latitude': latitude,
      'longitude': longitude,
      'address': address,
      'phone': phone,
      'distance': distance,
    };
  }

  String get distanceText {
    if (distance == null) return '';
    if (distance! < 1) {
      return '${(distance! * 1000).round()} m';
    }
    return '${distance!.toStringAsFixed(1)} km';
  }

  String get typeDisplay {
    switch (type) {
      case 'fire_station':
        return 'Fire Station';
      case 'hospital':
        return 'Hospital';
      case 'police':
        return 'Police Station';
      default:
        return type;
    }
  }

  static List<NearbyServiceModel> demoFireStations() {
    return [
      const NearbyServiceModel(
        id: 'fs-1',
        name: 'Delhi Fire Station #12',
        type: 'fire_station',
        latitude: 28.6139,
        longitude: 77.2090,
        address: 'Connaught Place, New Delhi',
        phone: '011-23412345',
        distance: 2.3,
      ),
      const NearbyServiceModel(
        id: 'fs-2',
        name: 'Delhi Fire Station #7',
        type: 'fire_station',
        latitude: 28.6448,
        longitude: 77.2167,
        address: 'Civil Lines, New Delhi',
        phone: '011-23456789',
        distance: 4.1,
      ),
      const NearbyServiceModel(
        id: 'fs-3',
        name: 'Gurugram Fire Station',
        type: 'fire_station',
        latitude: 28.4595,
        longitude: 77.0266,
        address: 'Sector 29, Gurugram',
        phone: '0124-2345678',
        distance: 8.5,
      ),
    ];
  }

  static List<NearbyServiceModel> demoHospitals() {
    return [
      const NearbyServiceModel(
        id: 'h-1',
        name: 'AIIMS Hospital',
        type: 'hospital',
        latitude: 28.5672,
        longitude: 77.2100,
        address: 'Ansari Nagar, New Delhi',
        phone: '011-26588500',
        distance: 1.8,
      ),
      const NearbyServiceModel(
        id: 'h-2',
        name: 'Safdarjung Hospital',
        type: 'hospital',
        latitude: 28.5685,
        longitude: 77.2066,
        address: 'Ring Road, New Delhi',
        phone: '011-26707437',
        distance: 3.2,
      ),
    ];
  }

  static List<NearbyServiceModel> demoPolice() {
    return [
      const NearbyServiceModel(
        id: 'p-1',
        name: 'Connaught Place Police Station',
        type: 'police',
        latitude: 28.6315,
        longitude: 77.2167,
        address: 'Connaught Place, New Delhi',
        phone: '011-23418888',
        distance: 1.5,
      ),
      const NearbyServiceModel(
        id: 'p-2',
        name: 'Parliament Street Police Station',
        type: 'police',
        latitude: 28.6196,
        longitude: 77.2127,
        address: 'Parliament Street, New Delhi',
        phone: '011-23366444',
        distance: 2.8,
      ),
    ];
  }
}
