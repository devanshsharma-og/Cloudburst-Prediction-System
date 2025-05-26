from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderServiceError, GeocoderUnavailable

def get_coordinates(location_name):
    """
    Uses GoogleV3 geocoder (IP-based quota) to look up lat/lon for a given place.
    No API key needed; will use Google’s free, rate-limited endpoint.
    """
    geolocator = GoogleV3(user_agent="weather_data_collector")
    try:
        # Timeout to avoid hanging indefinitely
        location = geolocator.geocode(location_name, timeout=10)
    except (GeocoderServiceError, GeocoderUnavailable) as e:
        print(f"[geocode] Service error for '{location_name}': {e}")
        return None, None
    if location:
        return location.latitude, location.longitude
    else:
        print(f"[geocode] Location '{location_name}' not found.")
        return None, None
