# Import necessary libraries
import streamlit as st
import pandas as pd
import requests
from sklearn.linear_model import LinearRegression

# Set Streamlit page configuration
st.set_page_config(page_title="Instant Quote Tool", layout="wide")

# Predefined cost multipliers by state
cost_multipliers = {
    "NY": 1.2,  # New York
    "CA": 2.5,  # California
    "IL": 1.5   # Illinois
}

# Function to get location info from the Zippopotam.us API
def get_location_info(zip_code):
    response = requests.get(f"https://api.zippopotam.us/us/{zip_code}")
    if response.status_code == 200:
        data = response.json()
        city = data['places'][0]['place name']
        state = data['places'][0]['state abbreviation']
        return city, state
    else:
        return None, None

# Sidebar navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Home 🏠", "Upload Data 📂", "Visualize Data 📊"])

# Home Page
if menu == "Home 🏠":
    st.title("Instant Quote Tool for Landscaping Services")
    st.markdown("Use this tool to get an instant quote based on property size, zip code, and type of service.")

    # Input fields
    zip_code = st.text_input("Enter Zip Code 🏙️", placeholder="E.g., 12345")
    property_size = st.number_input("Enter Property Size 📏 (in sq ft)", min_value=1000, max_value=50000, step=1000)
    service_type = st.selectbox("Select Service Type 🛠️", ["Lawn Care", "Tree Trimming", "Garden Maintenance"])

    # Get location info
    if zip_code:
        city, state = get_location_info(zip_code)
        if city and state:
            st.write(f"Location: {city}, {state}")
        else:
            st.error("Invalid Zip Code. Please enter a valid US zip code.")

        # Base quote prediction (example)
        base_quote = 500  # This would come from your model's prediction

        # Adjust the quote based on the state's cost multiplier
        if state in cost_multipliers:
            adjusted_quote = base_quote * cost_multipliers[state]
        else:
            adjusted_quote = base_quote

        # Display the adjusted quote
        st.success(f"Estimated Quote: ${adjusted_quote:.2f}")
