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
    "Lawn Care": {"base_rate": 0.10, "terrain_adjustment": {"Flat": 1.0, "Sloped": 1.2, "Mixed": 1.3}},
    "Tree Trimming": {"base_rate": 0.20, "terrain_adjustment": {"Flat": 1.0, "Sloped": 1.3, "Mixed": 1.4}},
    "Garden Maintenance": {"base_rate": 0.12, "terrain_adjustment": {"Flat": 1.0, "Sloped": 1.1, "Mixed": 1.3}},
    "Lawn Mowing": {"base_rate": 0.08, "terrain_adjustment": {"Flat": 1.0, "Sloped": 1.1, "Mixed": 1.2}},
}

# -----------------------------
# Location-Based Multipliers
# -----------------------------
location_multipliers = {
    "Urban": 1.3,
    "Suburban": 1.1,
    "Rural": 0.9
}

# Cost of Living Multipliers by State
cost_of_living_multipliers = {
    "NY": 1.4,
    "CA": 1.5,
    "TX": 1.1,
    "IL": 1.2,
    "FL": 1.1,
    "Average": 1.0
}

# -----------------------------
# Sidebar navigation
# -----------------------------
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Home 🏠", "Upload Data 📂", "Visualize Data 📊"])

# -----------------------------
# Function to calculate the quote
# -----------------------------
def calculate_quote(service_type, property_size, terrain_type, area_type, state):
    # Get service-specific base rate and terrain adjustment
    base_rate = service_pricing_factors[service_type]["base_rate"]
    terrain_multiplier = service_pricing_factors[service_type]["terrain_adjustment"][terrain_type]

    # Get location multiplier and cost of living adjustment
    location_multiplier = location_multipliers[area_type]
    cost_of_living_multiplier = cost_of_living_multipliers.get(state, 1.0)

    # Calculate the base quote
    base_quote = property_size * base_rate * terrain_multiplier

    # Adjust the quote based on location and cost of living
    adjusted_quote = base_quote * location_multiplier * cost_of_living_multiplier

    return adjusted_quote

# -----------------------------
# Stage 1: Home Page
# -----------------------------
if menu == "Home 🏠":
    st.title("Instant Quote Tool for Landscaping Services")
    st.markdown("Get an instant quote based on property size, zip code, and type of service.")

    # Input fields
    service_type = st.selectbox("Select Service Type 🛠️", list(service_pricing_factors.keys()))
    property_size = st.number_input("Enter Property Size 📏 (in sq ft)", min_value=1000, max_value=50000, step=1000)
    terrain_type = st.selectbox("Select Terrain Type 🌄", ["Flat", "Sloped", "Mixed"])
    area_type = st.selectbox("Select Area Type 🏙️", ["Urban", "Suburban", "Rural"])
    state = st.text_input("Enter State Abbreviation 🗺️", placeholder="E.g., NY, CA, TX")

    # Calculate the quote
    if st.button("Get Quote 🔘"):
        quote = calculate_quote(service_type, property_size, terrain_type, area_type, state)
        st.success(f"Estimated Quote: ${quote:.2f}")

        # Calculate confidence interval (95%)
        lower_bound = quote * 0.9
        upper_bound = quote * 1.1
        st.write(f"95% Confidence Interval: ${lower_bound:.2f} - ${upper_bound:.2f}")
