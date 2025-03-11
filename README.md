# Cloudburst-Prediction-System
# Weather Cloudburst Prediction App

This app leverages machine learning to predict cloudburst chances based on weather data. It collects weather data through Open Meteo API and uses Random Forest and Multiple Linear Regression models to predict the likelihood of a cloudburst occurring in a given location. The app displays the predictions along with visualizations.

## Features
- Fetches weather data for a specific location using the Open Meteo API.
- Uses machine learning models (Random Forest and Multiple Linear Regression) to predict the likelihood of a cloudburst.
- Visualizes actual rain vs. predicted cloudburst chances on a graph.
- Displays the predicted cloudburst chances in a table.

## Requirements

To run this app, you need the following Python packages:

- Streamlit
- pandas
- matplotlib
- scikit-learn
- requests

You can install them using the following command:

```bash
pip install streamlit pandas matplotlib scikit-learn requests
git clone <https://github.com/devanshsharma-og/Cloudburst-Prediction-System>
cd cloudburst_pred_sys
pip install -r requirements.txt
streamlit run app.py
