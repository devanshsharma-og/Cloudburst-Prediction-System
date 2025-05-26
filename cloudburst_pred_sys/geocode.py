from geopy.geocoders import Photon
from geopy.exc import GeocoderUnavailable, GeocoderTimedOut

def get_coordinates(location_name, timeout=10):
    """
    Uses the Photon geocoder to turn a place name into (lat, lon).
    Returns (latitude, longitude) or (None, None) on failure.
    """
    geolocator = Photon(user_agent="weather_data_collector", timeout=timeout)
    try:
        location = geolocator.geocode(location_name)
    except (GeocoderUnavailable, GeocoderTimedOut) as e:
        print(f"Geocoding service error: {e}")
        return None, None

    if location:
        return location.latitude, location.longitude
    else:
        print(f"Location '{location_name}' not found.")
        return None, None
