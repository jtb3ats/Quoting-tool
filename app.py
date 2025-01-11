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
# Function to get cost of living index from Numbeo API
# -----------------------------
@st.cache_data
def get_cost_of_living_index(city, state):
    api_key = "YOUR_NUMBEO_API_KEY"
    url = f"https://www.numbeo.com/api/cost_of_living?city={city}&country=USA&api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['cost_of_living_index']
    else:
        return 100  # Default value if API call fails

# -----------------------------
# Function to get median home value from a property API (Zillow/Redfin)
# -----------------------------
def get_median_home_value(zip_code):
    # Placeholder function - replace with real API call
    # For now, return a default value
    return 300000

# -----------------------------
# Function to get population density from US Census API
# -----------------------------
def get_population_density(zip_code):
    # Placeholder function - replace with real API call
    # For now, return a default value
    return 500  # People per square mile

# -----------------------------
# Function to calculate cost multiplier based on real-time data
# -----------------------------
def calculate_cost_multiplier(zip_code):
    city, state = get_location_info(zip_code)
    if city and state:
        cost_of_living_index = get_cost_of_living_index(city, state)
        median_home_value = get_median_home_value(zip_code)
        population_density = get_population_density(zip_code)

        # Apply the formula to calculate the cost multiplier
        cost_multiplier = (
            (cost_of_living_index / 100) * 0.4 +
            (median_home_value / 500000) * 0.3 +
            (population_density / 1000) * 0.2
        )

        return round(cost_multiplier, 2)
    else:
        return 1.0  # Default multiplier if location info is not available

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
    service_type = st.selectbox("Select Service Type 🛠️", ["Lawn Care", "Tree Trimming", "Garden Maintenance"])
    terrain_type = st.selectbox("Select Terrain Type 🌄", ["Flat", "Sloped", "Mixed"])

    # Calculate the cost multiplier
    if zip_code:
        cost_multiplier = calculate_cost_multiplier(zip_code)
        st.write(f"Cost Multiplier for {zip_code}: {cost_multiplier}")

        # Predefined dataset for demonstration
        data = {
            'Property Size (sq ft)': [5000, 10000, 15000, 20000],
            'Service Type': ["Lawn Care", "Tree Trimming", "Garden Maintenance", "Lawn Care"],
            'Terrain Type': ["Flat", "Sloped", "Mixed", "Flat"],
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
