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
# Function to calculate the cost multiplier
# -----------------------------
def calculate_cost_multiplier(zip_code):
    # Placeholder values - replace with real API calls if needed
    cost_of_living_index = 100  # Example: from Numbeo API
    median_home_value = 300000  # Example: from Zillow API
    population_density = 500  # Example: from Census API
    local_wages = 20  # Example: from BLS API

    # Calculate the cost multiplier using a weighted formula
    cost_multiplier = (
        (cost_of_living_index / 100) * 0.4 +
        (median_home_value / 500000) * 0.3 +
        (population_density / 1000) * 0.2 +
        (local_wages / 25) * 0.1
    )

    return round(cost_multiplier, 2)

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

    # Get location info
    if zip_code:
        city, state = get_location_info(zip_code)
        if city and state:
            st.write(f"Location: {city}, {state}")
        else:
            st.error("Invalid Zip Code. Please enter a valid US zip code.")

    # Calculate the cost multiplier
    cost_multiplier = calculate_cost_multiplier(zip_code)

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

    # Make the base prediction
    base_quote = model.predict([[property_size]])[0]

    # Adjust the quote based on the cost multiplier
    adjusted_quote = base_quote * cost_multiplier

    # Calculate confidence interval (95%)
    mse = mean_squared_error(y, model.predict(X))
    std_dev = np.sqrt(mse)
    lower_bound = adjusted_quote - 1.96 * std_dev
    upper_bound = adjusted_quote + 1.96 * std_dev

    # Display the adjusted quote with confidence interval
    if st.button("Get Quote 🔘"):
        st.success(f"Estimated Quote: ${adjusted_quote:.2f}")
        st.write(f"95% Confidence Interval: ${lower_bound:.2f} - ${upper_bound:.2f}")

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
    st.line_chart(df[['Property Size (sq ft)', 'Quote ($)']].set_index('Property Size (sq ft)'))
