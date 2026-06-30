"""
FireShield AI - Location Service

Provides nearby emergency services (fire stations, hospitals, police stations)
with realistic data for major Indian cities. Uses haversine formula for
distance calculations.
"""

from typing import List, Optional

from app.models.location import NearbyStation, NearbyHospital, NearbyPolice
from app.utils.helpers import haversine_distance


# ─────────────────────────────────────────────────────────────────────
# Fire Stations across major Indian cities
# ─────────────────────────────────────────────────────────────────────

_FIRE_STATIONS = [
    {"id": "FS001", "name": "Delhi Fire Station No. 1 - Connaught Place", "lat": 28.6304, "lng": 77.2177, "address": "Bhai Vir Singh Marg, Connaught Place, New Delhi 110001", "phone": "011-23411101", "available_units": 5},
    {"id": "FS002", "name": "Delhi Fire Station - Janak Puri", "lat": 28.6219, "lng": 77.0878, "address": "C-2 Block, Janak Puri, New Delhi 110058", "phone": "011-25504101", "available_units": 3},
    {"id": "FS003", "name": "Mumbai Fire Brigade HQ - Byculla", "lat": 18.9788, "lng": 72.8330, "address": "Dr. Babasaheb Ambedkar Rd, Byculla, Mumbai 400027", "phone": "022-23076111", "available_units": 8},
    {"id": "FS004", "name": "Mumbai Fire Station - Andheri", "lat": 19.1136, "lng": 72.8697, "address": "S.V. Road, Andheri West, Mumbai 400058", "phone": "022-26282101", "available_units": 4},
    {"id": "FS005", "name": "Bangalore Fire Station - Koramangala", "lat": 12.9346, "lng": 77.6267, "address": "80 Feet Road, Koramangala, Bangalore 560034", "phone": "080-25520333", "available_units": 4},
    {"id": "FS006", "name": "Bangalore Fire Station - Whitefield", "lat": 12.9698, "lng": 77.7499, "address": "ITPL Main Road, Whitefield, Bangalore 560066", "phone": "080-28452101", "available_units": 3},
    {"id": "FS007", "name": "Chennai Fire & Rescue HQ - Egmore", "lat": 13.0732, "lng": 80.2609, "address": "Pantheon Road, Egmore, Chennai 600008", "phone": "044-25361101", "available_units": 6},
    {"id": "FS008", "name": "Chennai Fire Station - T. Nagar", "lat": 13.0418, "lng": 80.2337, "address": "Usman Road, T. Nagar, Chennai 600017", "phone": "044-24341101", "available_units": 3},
    {"id": "FS009", "name": "Kolkata Fire Brigade HQ - Central Avenue", "lat": 22.5726, "lng": 88.3639, "address": "7 Central Avenue, Kolkata 700073", "phone": "033-22861101", "available_units": 5},
    {"id": "FS010", "name": "Hyderabad Fire Station - Abids", "lat": 17.3925, "lng": 78.4753, "address": "Abids Circle, Hyderabad 500001", "phone": "040-24756101", "available_units": 4},
    {"id": "FS011", "name": "Pune Fire Brigade - Swargate", "lat": 18.5018, "lng": 73.8636, "address": "Swargate, Pune 411009", "phone": "020-24268101", "available_units": 4},
    {"id": "FS012", "name": "Jaipur Fire Station - MI Road", "lat": 26.9124, "lng": 75.7873, "address": "MI Road, Jaipur 302001", "phone": "0141-2560101", "available_units": 3},
    {"id": "FS013", "name": "Lucknow Fire Station - Hazratganj", "lat": 26.8500, "lng": 80.9500, "address": "Hazratganj, Lucknow 226001", "phone": "0522-2623101", "available_units": 4},
    {"id": "FS014", "name": "Ahmedabad Fire Station - Ellis Bridge", "lat": 23.0300, "lng": 72.5700, "address": "Ellis Bridge, Ahmedabad 380006", "phone": "079-25390101", "available_units": 5},
    {"id": "FS015", "name": "Delhi Fire Station - Rohini", "lat": 28.7495, "lng": 77.0565, "address": "Sector 16, Rohini, New Delhi 110089", "phone": "011-27555101", "available_units": 3},
]


# ─────────────────────────────────────────────────────────────────────
# Hospitals across major Indian cities
# ─────────────────────────────────────────────────────────────────────

_HOSPITALS = [
    {"id": "H001", "name": "AIIMS - All India Institute of Medical Sciences", "lat": 28.5672, "lng": 77.2100, "address": "Sri Aurobindo Marg, Ansari Nagar, New Delhi 110029", "phone": "011-26588500", "emergency_available": True, "burn_unit": True},
    {"id": "H002", "name": "Safdarjung Hospital", "lat": 28.5685, "lng": 77.2066, "address": "Ansari Nagar West, New Delhi 110029", "phone": "011-26707437", "emergency_available": True, "burn_unit": True},
    {"id": "H003", "name": "KEM Hospital", "lat": 19.0003, "lng": 72.8422, "address": "Acharya Donde Marg, Parel, Mumbai 400012", "phone": "022-24136051", "emergency_available": True, "burn_unit": True},
    {"id": "H004", "name": "Lilavati Hospital", "lat": 19.0509, "lng": 72.8294, "address": "A-791, Bandra Reclamation, Mumbai 400050", "phone": "022-26568000", "emergency_available": True, "burn_unit": False},
    {"id": "H005", "name": "St. John's Medical College Hospital", "lat": 12.9280, "lng": 77.6208, "address": "Sarjapur Road, Koramangala, Bangalore 560034", "phone": "080-22065000", "emergency_available": True, "burn_unit": True},
    {"id": "H006", "name": "Victoria Hospital", "lat": 12.9567, "lng": 77.5731, "address": "Fort Road, K.R. Market, Bangalore 560002", "phone": "080-26701150", "emergency_available": True, "burn_unit": True},
    {"id": "H007", "name": "Apollo Hospital - Chennai", "lat": 13.0067, "lng": 80.2206, "address": "21 Greams Lane, Off Greams Road, Chennai 600006", "phone": "044-28293333", "emergency_available": True, "burn_unit": True},
    {"id": "H008", "name": "SSKM Hospital - Kolkata", "lat": 22.5389, "lng": 88.3448, "address": "244 AJC Bose Road, Kolkata 700020", "phone": "033-22041101", "emergency_available": True, "burn_unit": True},
    {"id": "H009", "name": "NIMS Hospital - Hyderabad", "lat": 17.3948, "lng": 78.3942, "address": "Punjagutta, Hyderabad 500082", "phone": "040-23489000", "emergency_available": True, "burn_unit": True},
    {"id": "H010", "name": "Sassoon General Hospital - Pune", "lat": 18.5155, "lng": 73.8740, "address": "Sassoon Road, Pune 411001", "phone": "020-26128000", "emergency_available": True, "burn_unit": True},
    {"id": "H011", "name": "SMS Hospital - Jaipur", "lat": 26.8988, "lng": 75.8064, "address": "Jaipur 302004", "phone": "0141-2518501", "emergency_available": True, "burn_unit": True},
    {"id": "H012", "name": "KGMU Hospital - Lucknow", "lat": 26.8569, "lng": 80.9407, "address": "Shah Mina Road, Lucknow 226003", "phone": "0522-2257540", "emergency_available": True, "burn_unit": True},
    {"id": "H013", "name": "Civil Hospital - Ahmedabad", "lat": 23.0465, "lng": 72.6006, "address": "Asarwa, Ahmedabad 380016", "phone": "079-22683721", "emergency_available": True, "burn_unit": True},
]


# ─────────────────────────────────────────────────────────────────────
# Police Stations across major Indian cities
# ─────────────────────────────────────────────────────────────────────

_POLICE_STATIONS = [
    {"id": "P001", "name": "Parliament Street Police Station", "lat": 28.6237, "lng": 77.2138, "address": "Parliament Street, New Delhi 110001", "phone": "011-23361600"},
    {"id": "P002", "name": "Saket Police Station", "lat": 28.5244, "lng": 77.2067, "address": "Press Enclave Marg, Saket, New Delhi 110017", "phone": "011-26864400"},
    {"id": "P003", "name": "Colaba Police Station", "lat": 18.9067, "lng": 72.8147, "address": "Shahid Bhagat Singh Marg, Colaba, Mumbai 400005", "phone": "022-22821824"},
    {"id": "P004", "name": "Bandra Police Station", "lat": 19.0544, "lng": 72.8402, "address": "Hill Road, Bandra West, Mumbai 400050", "phone": "022-26422242"},
    {"id": "P005", "name": "Koramangala Police Station", "lat": 12.9340, "lng": 77.6260, "address": "80 Feet Road, Koramangala, Bangalore 560034", "phone": "080-25520242"},
    {"id": "P006", "name": "HSR Layout Police Station", "lat": 12.9116, "lng": 77.6474, "address": "27th Main Road, HSR Layout, Bangalore 560102", "phone": "080-25731242"},
    {"id": "P007", "name": "Thousand Lights Police Station", "lat": 13.0552, "lng": 80.2535, "address": "Anna Salai, Chennai 600006", "phone": "044-28464242"},
    {"id": "P008", "name": "Lal Bazaar Police HQ - Kolkata", "lat": 22.5673, "lng": 88.3496, "address": "36, Lal Bazar Street, Kolkata 700001", "phone": "033-22143230"},
    {"id": "P009", "name": "Abids Police Station - Hyderabad", "lat": 17.3937, "lng": 78.4749, "address": "Abids, Hyderabad 500001", "phone": "040-27853242"},
    {"id": "P010", "name": "Swargate Police Station - Pune", "lat": 18.4996, "lng": 73.8643, "address": "Swargate, Pune 411009", "phone": "020-26433242"},
    {"id": "P011", "name": "MI Road Police Station - Jaipur", "lat": 26.9118, "lng": 75.7866, "address": "MI Road, Jaipur 302001", "phone": "0141-2570100"},
    {"id": "P012", "name": "Hazratganj Police Station - Lucknow", "lat": 26.8494, "lng": 80.9488, "address": "Hazratganj, Lucknow 226001", "phone": "0522-2620242"},
]


def find_nearby_fire_stations(
    lat: float, lng: float, radius_km: float = 10.0, limit: int = 5
) -> List[NearbyStation]:
    """
    Find fire stations near a given location.

    Args:
        lat: Query latitude.
        lng: Query longitude.
        radius_km: Search radius in kilometers.
        limit: Maximum number of results.

    Returns:
        List of NearbyStation objects sorted by distance.
    """
    results = []
    for station in _FIRE_STATIONS:
        distance = haversine_distance(lat, lng, station["lat"], station["lng"])
        if distance <= radius_km:
            results.append(NearbyStation(
                id=station["id"],
                name=station["name"],
                lat=station["lat"],
                lng=station["lng"],
                address=station["address"],
                phone=station["phone"],
                distance_km=distance,
                available_units=station["available_units"],
            ))

    results.sort(key=lambda x: x.distance_km)
    return results[:limit]


def find_nearby_hospitals(
    lat: float, lng: float, radius_km: float = 10.0, limit: int = 5
) -> List[NearbyHospital]:
    """
    Find hospitals near a given location.

    Args:
        lat: Query latitude.
        lng: Query longitude.
        radius_km: Search radius in kilometers.
        limit: Maximum number of results.

    Returns:
        List of NearbyHospital objects sorted by distance.
    """
    results = []
    for hospital in _HOSPITALS:
        distance = haversine_distance(lat, lng, hospital["lat"], hospital["lng"])
        if distance <= radius_km:
            results.append(NearbyHospital(
                id=hospital["id"],
                name=hospital["name"],
                lat=hospital["lat"],
                lng=hospital["lng"],
                address=hospital["address"],
                phone=hospital["phone"],
                distance_km=distance,
                emergency_available=hospital["emergency_available"],
                burn_unit=hospital["burn_unit"],
            ))

    results.sort(key=lambda x: x.distance_km)
    return results[:limit]


def find_nearby_police(
    lat: float, lng: float, radius_km: float = 10.0, limit: int = 5
) -> List[NearbyPolice]:
    """
    Find police stations near a given location.

    Args:
        lat: Query latitude.
        lng: Query longitude.
        radius_km: Search radius in kilometers.
        limit: Maximum number of results.

    Returns:
        List of NearbyPolice objects sorted by distance.
    """
    results = []
    for station in _POLICE_STATIONS:
        distance = haversine_distance(lat, lng, station["lat"], station["lng"])
        if distance <= radius_km:
            results.append(NearbyPolice(
                id=station["id"],
                name=station["name"],
                lat=station["lat"],
                lng=station["lng"],
                address=station["address"],
                phone=station["phone"],
                distance_km=distance,
            ))

    results.sort(key=lambda x: x.distance_km)
    return results[:limit]
