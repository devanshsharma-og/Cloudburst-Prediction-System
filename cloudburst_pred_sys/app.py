import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
from datetime import datetime

from weather_data import fetch_weather_data, generate_synthetic_data
from geocode import get_coordinates
from ml_model import train_random_forest_regressor, train_mlr_model
import random

# Streamlit UI setup
st.title("Weather Data Collector")
st.sidebar.title("Control Panel")

# Take location input from Streamlit sidebar
location_name = st.sidebar.text_input("Location Name", placeholder="Enter a location (e.g., Berlin)")

# Button to generate data
generate_button = st.sidebar.button("Generate Weather Data")

# Button to display combined data before MLR model
display_combined_button = st.sidebar.button("Display Combined Data")

# Button to run MLR model
run_mlr_button = st.sidebar.button("Run MLR Model")

# Create an empty space for graph display
st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
graph_placeholder = st.empty()
st.markdown("</div>", unsafe_allow_html=True)

if location_name and generate_button:
    # Clear previous data in session state
    if 'weather_data' in st.session_state:
        del st.session_state.weather_data
    if 'predictions' in st.session_state:
        del st.session_state.predictions

    try:
        latitude, longitude = get_coordinates(location_name)
    except Exception as e:
        latitude, longitude = None, None

    if latitude is None or longitude is None:
        st.error("Unable to retrieve coordinates for the given location. Please check your network or try another place.")
    else:
        st.sidebar.write(f"Coordinates for {location_name}: {latitude:.5f}°N, {longitude:.5f}°E")

        # Fetch weather data
        weather_data = fetch_weather_data(latitude, longitude)

        # Generate synthetic data
        synthetic_data = generate_synthetic_data(len(weather_data["hourly_data"]["cloud_cover_high"]))

        # Store the data in session state
        st.session_state.weather_data = weather_data
        # Merge synthetic into hourly
        st.session_state.weather_data["hourly_data"].update(synthetic_data)

        st.sidebar.success("Weather data has been successfully generated.")

if display_combined_button:
    if 'weather_data' in st.session_state:
        combined_data = pd.DataFrame(st.session_state.weather_data['hourly_data'])
        st.write(combined_data)
    else:
        st.sidebar.error("Weather data not available. Please generate data first.")

if run_mlr_button:
    if 'weather_data' in st.session_state:
        # Extract combined data
        combined_data = pd.DataFrame(st.session_state.weather_data['hourly_data'])

        # Train Random Forest Regressor
        rf_regressor, predictions = train_random_forest_regressor(st.session_state.weather_data)

        # Run MLR Model after RF predictions
        mlr_predictions = train_mlr_model(st.session_state.weather_data, predictions)

        # Flatten arrays
        mlr_predictions = mlr_predictions.flatten()

        # Make sure dates are plain numpy array
        if isinstance(combined_data["date"], pd.Series):
            combined_data["date"] = combined_data["date"].values

        # Check length consistency
        if len(mlr_predictions) == len(combined_data["date"]):
            actual_rain = combined_data["rain"]
            if len(actual_rain) == len(mlr_predictions):
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(combined_data["date"], actual_rain, label='Actual Rain (mm)', marker='o')
                ax.plot(combined_data["date"], mlr_predictions, label='Predicted Cloudburst Chance (%)', marker='x')
                ax.set_xlabel('Date')
                ax.set_ylabel('Value')
                ax.set_title('Actual Rain vs Predicted Cloudburst Chance')
                ax.legend()
                plt.xticks(rotation=45)
                graph_placeholder.pyplot(fig)

                st.write("Predicted Cloudburst Chances (from MLR model):")
                st.write(pd.DataFrame({
                    "Date": combined_data["date"],
                    "Predicted Cloudburst Chance (%)": mlr_predictions
                }))
            else:
                st.error("The lengths of actual rain and predictions do not match.")
        else:
            st.error("The length of the predictions and dates do not match.")
    else:
        st.sidebar.error("Weather data not available. Please generate data first.")
