import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable, GeocoderTimedOut

def get_coordinates(location_name, max_retries=3, pause_seconds=1):
    """
    Return (latitude, longitude) for the given location_name.
    Retries up to max_retries times on temporary failures.
    Returns (None, None) if lookup fails or location not found.
    """
    geolocator = Nominatim(user_agent="weather_data_collector", timeout=10)
    for attempt in range(1, max_retries + 1):
        try:
            loc = geolocator.geocode(location_name)
            if loc:
                return loc.latitude, loc.longitude
            # valid response but nothing found
            return None, None

        except (GeocoderTimedOut, GeocoderUnavailable) as exc:
            # on last attempt, give up
            if attempt == max_retries:
                return None, None
            # otherwise back off and retry
            time.sleep(pause_seconds)

    # fallback
    return None, None
