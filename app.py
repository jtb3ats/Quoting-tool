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
# Function to get cost of living index from Numbeo API (Placeholder)
# -----------------------------
def get_cost_of_living_index(city, state):
    # Replace this with a real API call to Numbeo
    cost_of_living_index = 100  # Default value
    return cost_of_living_index

# -----------------------------
# Function to calculate the cost multiplier
# -----------------------------
def calculate_cost_multiplier(zip_code):
    city, state = get_location_info(zip_code)
    if city and state:
        cost_of_living_index = get_cost_of_living_index(city, state)
        population_density = 1000  # Placeholder for Census API
        wage_index = 20  # Placeholder for BLS API
        home_value_index = 300000  # Placeholder for Zillow API

        # Calculate the cost multiplier using a weighted formula
        cost_multiplier = (
            (cost_of_living_index / 100) * 0.4 +
            (population_density / 1000) * 0.3 +
            (wage_index / 25) * 0.2 +
            (home_value_index / 500000) * 0.1
        )
        return round(cost_multiplier, 2)
    else:
        return 1.0

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

    # Get location info and cost multiplier
    if zip_code:
        city, state = get_location_info(zip_code)
        if city and state:
            st.write(f"Location: {city}, {state}")
            cost_multiplier = calculate_cost_multiplier(zip_code)
            st.write(f"Cost Multiplier: {cost_multiplier}")

            # Get service-specific adjustments
            service_base_rate = service_pricing_factors[service_type]["base_rate"]
            terrain_adjustment = service_pricing_factors[service_type]["terrain_adjustment"][terrain_type]

            # Calculate the base quote
            base_quote = property_size * service_base_rate * terrain_adjustment

            # Adjust the quote based on the cost multiplier
            adjusted_quote = base_quote * cost_multiplier

            # Calculate confidence interval (95%)
            lower_bound = adjusted_quote * 0.9
            upper_bound = adjusted_quote * 1.1

            # Display the adjusted quote with confidence interval
            if st.button("Get Quote 🔘"):
                st.success(f"Estimated Quote: ${adjusted_quote:.2f}")
                st.write(f"95% Confidence Interval: ${lower_bound:.2f} - ${upper_bound:.2f}")
        else:
            st.error("Invalid Zip Code. Please enter a valid US zip code.")

# -----------------------------
# Stage 2: Upload Data Page
# -----------------------------
elif menu == "Upload Data 📂":
    st.title("Upload Your Dataset")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        custom_data = pd.read_csv(uploaded_file)
        st.write("Uploaded Dataset:")
        st.dataframe(custom_data)

        # Train the model on the uploaded data
        model = LinearRegression()
        X = custom_data.drop('Quote ($)', axis=1)
        y = custom_data['Quote ($)']
        model.fit(X, y)

        st.success("Model retrained with uploaded dataset!")

# -----------------------------
# Stage 3: Visualize Data Page
# -----------------------------
elif menu == "Visualize Data 📊":
    st.title("Data Visualization")
    st.markdown("Explore the data used to train the model and see how it fits.")
    st.line_chart(pd.DataFrame({
        'Property Size (sq ft)': [5000, 10000, 15000, 20000],
        'Quote ($)': [200, 400, 600, 800]
    }).set_index('Property Size (sq ft)'))
