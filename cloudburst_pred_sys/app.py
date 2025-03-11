import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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

    latitude, longitude = get_coordinates(location_name)

    if latitude is None or longitude is None:
        st.error("Unable to retrieve coordinates for the given location.")
    else:
        st.sidebar.write(f"Coordinates for {location_name}: {latitude}°N, {longitude}°E")

        # Fetch weather data
        weather_data = fetch_weather_data(latitude, longitude)

        # Generate synthetic data
        synthetic_data = generate_synthetic_data(len(weather_data["hourly_data"]["cloud_cover_high"]))

        # Store the data in session state
        st.session_state.weather_data = weather_data
        # Assuming synthetic data is being merged into hourly data
        st.session_state.weather_data["hourly_data"].update(synthetic_data)

        st.sidebar.success("Weather data has been successfully generated.")

if display_combined_button:
    if 'weather_data' in st.session_state:
        # Assuming 'hourly_data' is part of the 'weather_data'
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

        # Run MLR Model after Random Forest predictions
        mlr_predictions = train_mlr_model(st.session_state.weather_data, predictions)

        # Ensure mlr_predictions is 1-dimensional
        mlr_predictions = mlr_predictions.flatten()  # Make sure it's 1D

        # Ensure combined_data["date"] is 1-dimensional
        if isinstance(combined_data["date"], pd.Series):
            combined_data["date"] = combined_data["date"].values  # Make it 1D if it's a Series

        # Check if lengths match
        if len(mlr_predictions) == len(combined_data["date"]):
            # Create a plot for the MLR model predictions vs actual rain
            # Get actual rain values from the weather data (assumed key: 'rain' in 'hourly_data')
            actual_rain = combined_data["rain"]  # Assuming 'rain' is the target variable in the dataset
            
            if len(actual_rain) == len(mlr_predictions):
                fig, ax = plt.subplots(figsize=(10, 6))

                ax.plot(combined_data["date"], actual_rain, label='Actual Rain (mm)', color='blue', marker='o')
                ax.plot(combined_data["date"], mlr_predictions, label='Predicted Cloudburst Chance (%)', color='orange', marker='x')
                
                # Formatting the plot
                ax.set_xlabel('Date')
                ax.set_ylabel('Value')
                ax.set_title('Actual Rain vs Predicted Cloudburst Chance')
                ax.legend()

                # Rotate the date labels for better readability
                plt.xticks(rotation=45)
                graph_placeholder.pyplot(fig)  # Display the plot in Streamlit
            else:
                st.error("The lengths of actual rain and predictions do not match.")

            # Display the predicted cloudburst chance dataset below the graph
            st.write("Predicted Cloudburst Chances (from MLR model):")
            st.write(pd.DataFrame({"Date": combined_data["date"], "Predicted Cloudburst Chance (%)": mlr_predictions}))
        else:
            st.error("The length of the predictions and dates do not match.")
    else:
        st.sidebar.error("Weather data not available. Please generate data first.")
