from geopy.geocoders import Nominatim

def get_coordinates(location_name):
    geolocator = Nominatim(user_agent="weather_data_collector")
    location = geolocator.geocode(location_name)
    if location:
        return location.latitude, location.longitude
    else:
        print("Location not found.")
        return None, None