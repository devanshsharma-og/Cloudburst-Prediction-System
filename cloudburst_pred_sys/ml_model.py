import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor

def train_random_forest_regressor(weather_data):
    """ Trains the Random Forest model and returns predictions. """
    features = [
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
    targets = [
        "cloud_density", "ppm_content", "dust_particle_analysis", "chemical_content_in_clouds", 
        "cloud_darkness_albedo_optical_depth", "moisture_holding_capacity", "cloud_top_temperature", 
        "cloud_top_height"
    ]

    # Extracting 'hourly_data' from weather_data
    hourly_data = weather_data.get('hourly_data', {})
    
    # Exclude non-numeric columns (e.g., datetime)
    feature_data = pd.DataFrame({feature: hourly_data.get(feature, []) for feature in features})
    target_data = pd.DataFrame({target: hourly_data.get(target, []) for target in targets})

    rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_regressor.fit(feature_data, target_data)

    predictions = rf_regressor.predict(feature_data)
    return rf_regressor, predictions

def train_mlr_model(weather_data, predictions):
    """Trains the MLR model and returns predictions."""
    features = [
        "temperature_2m", "relative_humidity_2m", "dew_point_2m", "apparent_temperature", 
        "precipitation_probability", "precipitation", "showers", "snowfall", 
        "snow_depth", "weather_code", "pressure_msl", "surface_pressure", "cloud_cover", 
        "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high", "visibility", 
        "evapotranspiration", "et0_fao_evapotranspiration", "wind_speed_10m", "wind_speed_80m", 
        "wind_speed_120m", "wind_speed_180m", "wind_direction_10m", "wind_direction_80m", 
        "wind_direction_120m", "wind_direction_180m", "wind_gusts_10m", "temperature_80m", 
        "temperature_120m", "temperature_180m", "soil_temperature_0cm", "soil_temperature_6cm", 
        "soil_temperature_18cm", "soil_temperature_54cm", "soil_moisture_0_to_1cm", 
        "soil_moisture_1_to_3cm", "soil_moisture_3_to_9cm", "soil_moisture_9_to_27cm", 
        "soil_moisture_27_to_81cm", "cloud_density", "ppm_content", "dust_particle_analysis", 
        "chemical_content_in_clouds", "cloud_darkness_albedo_optical_depth", "moisture_holding_capacity", 
        "cloud_top_temperature", "cloud_top_height"
    ]
    target = "rain"

    # Normalize features
    hourly_data = weather_data.get('hourly_data', {})
    
    # Exclude non-numeric columns (e.g., datetime)
    X = pd.DataFrame(hourly_data).select_dtypes(include=[np.number]).fillna(0)
    y = pd.DataFrame(hourly_data.get(target, []), columns=[target]).fillna(0)

    # Normalize the features
    scaler = MinMaxScaler()
    X_normalized = scaler.fit_transform(X)

    lr_model = LinearRegression()
    lr_model.fit(X_normalized, y)

    # Predict cloudburst chance
    y_pred = lr_model.predict(X_normalized)
    y_pred_clb = np.clip(y_pred, 0, 100)

    return y_pred_clb
