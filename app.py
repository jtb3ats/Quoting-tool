# Import necessary libraries
import streamlit as st
import pandas as pd
import requests
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Set Streamlit page configuration
st.set_page_config(page_title="Instant Quote Tool", layout="wide")

# -----------------------------
# Service-Specific Pricing Adjustments
# -----------------------------
service_pricing_factors = {
    "Lawn Care": {"base_rate": 0.1, "terrain_adjustment": {"Flat": 1.0, "Sloped": 1.2, "Mixed": 1.5}},
    "Tree Trimming": {"base_rate": 0.15, "terrain_adjustment": {"Flat": 1.0, "Sloped": 1.3, "Mixed": 1.6}},
    "Garden Maintenance": {"base_rate": 0.12, "terrain_adjustment": {"Flat": 1.0, "Sloped": 1.1, "Mixed": 1.4}},
}

# -----------------------------
# Function to get location info from Zippopotam.us API
# -----------------------------
@st.cache_data
def get_location_info(zip_code):
    response = requests.get(f"https://api.zippopotam.us/us/{zip_code}")
    if response.status_code == 200:
        data = response.json()
        city = data['places'][0]['place name']
        state = data['places'][0]['state abbreviation']
        return city, state
    else:
        return None, None

# -----------------------------
# Function to calculate the cost multiplier
# -----------------------------
def calculate_cost_multiplier(zip_code, service_type, terrain_type):
    city, state = get_location_info(zip_code)
    
    # Placeholder real-time factors (replace with real API calls)
    cost_of_living_index = 100  # Replace with API call to Numbeo
    median_home_value = 300000  # Replace with API call to Zillow/Redfin
    population_density = 500  # Replace with API call to US Census
    local_wages = 20  # Replace with API call to BLS

    # Calculate the cost multiplier
    cost_multiplier = (
        (cost_of_living_index / 100) * 0.4 +
        (median_home_value / 500000) * 0.3 +
        (population_density / 1000) * 0.2 +
        (local_wages / 25) * 0.1
    )

    # Apply service-specific and terrain-specific adjustments
    service_factor = service_pricing_factors.get(service_type, {}).get("base_rate", 1.0)
    terrain_factor = service_pricing_factors.get(service_type, {}).get("terrain_adjustment", {}).get(terrain_type, 1.0)

    # Final multiplier
    final_multiplier = cost_multiplier * service_factor * terrain_factor
    return round(final_multiplier, 2)

# -----------------------------
# Sidebar navigation
# -----------------------------
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Home 🏠", "Upload Data 📂", "Visualize Data 📊"])

# -----------------------------
# Stage 1: Home Page
# -----------------------------
if menu == "Home 🏠":
    st.title("Instant Quote Tool for Landscaping Services")
    st.markdown("Get an instant quote based on property size, zip code, and type of service.")

    # Input fields
    zip_code = st.text_input("Enter Zip Code 🏙️", placeholder="E.g., 12345")
    property_size = st.number_input("Enter Property Size 📏 (in sq ft)", min_value=1000, max_value=50000, step=1000)
    service_type = st.selectbox("Select Service Type 🛠️", list(service_pricing_factors.keys()))
    terrain_type = st.selectbox("Select Terrain Type 🌄", ["Flat", "Sloped", "Mixed"])

    # Calculate the cost multiplier
    if zip_code:
        cost_multiplier = calculate_cost_multiplier(zip_code, service_type, terrain_type)
        st.write(f"Cost Multiplier for {zip_code}: {cost_multiplier}")

        # Predefined dataset for demonstration
        data = {
            'Property Size (sq ft)': [5000, 10000, 15000, 20000],
            'Quote ($)': [200, 400, 600, 800]
        }
        df = pd.DataFrame(data)

        # Train a model on the predefined data
        model = LinearRegression()
        X = df[['Property Size (sq ft)']]
        y = df['Quote ($)']
        model.fit(X, y)

        # Make the prediction
        base_quote = model.predict([[property_size]])[0]
        adjusted_quote = base_quote * cost_multiplier

        # Display the adjusted quote
        st.success(f"Estimated Quote: ${adjusted_quote:.2f}")
