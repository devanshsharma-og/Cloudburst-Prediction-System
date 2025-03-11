import openmeteo_requests
import random
import pandas as pd
from datetime import datetime

# Setup the Open-Meteo API client
openmeteo = openmeteo_requests.Client()

def fetch_weather_data(latitude, longitude):
    """ Fetches weather data from Open-Meteo API """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": [
            "temperature_2m", "relative_humidity_2m", "dew_point_2m", "apparent_temperature", 
            "precipitation_probability", "precipitation", "rain", "showers", "snowfall", 
            "snow_depth", "weather_code", "pressure_msl", "surface_pressure", "cloud_cover", 
            "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high", "visibility", 
            "evapotranspiration", "et0_fao_evapotranspiration", "wind_speed_10m", "wind_speed_80m", 
            "wind_speed_120m", "wind_speed_180m", "wind_direction_10m", "wind_direction_80m", 
            "wind_direction_120m", "wind_direction_180m", "wind_gusts_10m", "temperature_80m", 
            "temperature_120m", "temperature_180m", "soil_temperature_0cm", "soil_temperature_6cm", 
            "soil_temperature_18cm", "soil_temperature_54cm", "soil_moisture_0_to_1cm", 
            "soil_moisture_1_to_3cm", "soil_moisture_3_to_9cm", "soil_moisture_9_to_27cm", 
            "soil_moisture_27_to_81cm"
        ]
    }

    # Fetch data from the Open-Meteo API
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    hourly = response.Hourly()
    hourly_data = {
        "location": {
            "latitude": response.Latitude(),
            "longitude": response.Longitude(),
            "elevation": response.Elevation(),
            "timezone": response.Timezone(),
            "timezone_abbreviation": response.TimezoneAbbreviation(),
            "utc_offset_seconds": response.UtcOffsetSeconds()
        },
        "timestamp": datetime.utcnow(),
        "hourly_data": {}
    }

    hourly_variables = [
        "temperature_2m", "relative_humidity_2m", "dew_point_2m", "apparent_temperature", 
        "precipitation_probability", "precipitation", "rain", "showers", "snowfall", 
        "snow_depth", "weather_code", "pressure_msl", "surface_pressure", "cloud_cover", 
        "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high", "visibility", 
        "evapotranspiration", "et0_fao_evapotranspiration", "wind_speed_10m", "wind_speed_80m", 
        "wind_speed_120m", "wind_speed_180m", "wind_direction_10m", "wind_direction_80m", 
        "wind_direction_120m", "wind_direction_180m", "wind_gusts_10m", "temperature_80m", 
        "temperature_120m", "temperature_180m", "soil_temperature_0cm", "soil_temperature_6cm", 
        "soil_temperature_18cm", "soil_temperature_54cm", "soil_moisture_0_to_1cm", 
        "soil_moisture_1_to_3cm", "soil_moisture_3_to_9cm", "soil_moisture_9_to_27cm", 
        "soil_moisture_27_to_81cm"
    ]

    for idx, var in enumerate(hourly_variables):
        hourly_data["hourly_data"][var] = hourly.Variables(idx).ValuesAsNumpy().tolist()

    hourly_data["hourly_data"]["date"] = pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    ).tolist()

    return hourly_data

def generate_synthetic_data(num_rows):
    """Generates synthetic data for various weather parameters."""
    return {
        "cloud_density": [round(random.uniform(0, 1), 2) for _ in range(num_rows)],
        "ppm_content": [random.randint(100, 500) for _ in range(num_rows)],
        "dust_particle_analysis": [round(random.uniform(0, 500), 2) for _ in range(num_rows)],
        "chemical_content_in_clouds": [round(random.uniform(0, 1), 3) for _ in range(num_rows)],
        "cloud_darkness_albedo_optical_depth": [round(random.uniform(0.3, 0.9), 2) for _ in range(num_rows)],
        "moisture_holding_capacity": [round(random.uniform(0.2, 0.6), 2) for _ in range(num_rows)],
        "cloud_top_temperature": [round(random.uniform(-50, 0), 2) for _ in range(num_rows)],
        "cloud_top_height": [round(random.uniform(8000, 15000), 0) for _ in range(num_rows)],
    }
