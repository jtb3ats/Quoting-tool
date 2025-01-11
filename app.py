# Import necessary libraries
import streamlit as st
import pandas as pd
import requests
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Set Streamlit page configuration
st.set_page_config(page_title="Instant Quote Tool", layout="wide")

# Predefined cost multipliers by state (can be overridden by API data)
cost_multipliers = {
    "NY": 1.2,
    "CA": 2.5,
    "IL": 1.5
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
# Function to get cost of living adjustment
# (Replace with your chosen API - example is Numbeo)
# -----------------------------
@st.cache_data
def get_cost_of_living(zip_code):
    # Example: Replace with actual API call
    # For now, return a static value based on state
    state_cost_multiplier = {
        "NY": 1.3,
        "CA": 1.5,
        "TX": 1.1
    }
    _, state = get_location_info(zip_code)
    return state_cost_multiplier.get(state, 1.0)

# -----------------------------
# Sidebar navigation
# -----------------------------
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Home 🏠", "Upload Data 📂", "Visualize Data 📊"])

# -----------------------------
# Function to train the model and calculate confidence intervals
# -----------------------------
def train_model(data):
    data_encoded = pd.get_dummies(data, columns=['Service Type', 'Terrain Type'])
    X = data_encoded.drop('Quote ($)', axis=1)
    y = data_encoded['Quote ($)']
    
    model = LinearRegression()
    model.fit(X, y)

    # Calculate prediction errors for confidence interval
    y_pred = model.predict(X)
    errors = y - y_pred
    mse = mean_squared_error(y, y_pred)
    std_dev = np.std(errors)
    return model, X, mse, std_dev

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

        # Get cost of living adjustment
        cost_of_living = get_cost_of_living(zip_code)
        st.write(f"Cost of Living Adjustment: {cost_of_living}")

    # Predefined dataset for demonstration
    data = {
        'Zip Code': [12345, 12346, 12347, 12348],
        'Property Size (sq ft)': [5000, 10000, 15000, 20000],
        'Service Type': ["Lawn Care", "Tree Trimming", "Garden Maintenance", "Lawn Care"],
        'Terrain Type': ["Flat", "Sloped", "Mixed", "Flat"],
        'Quote ($)': [200, 400, 600, 800]
    }
    df = pd.DataFrame(data)

    # Train a model on the predefined data
    model, X, mse, std_dev = train_model(df)

    # Create input DataFrame for prediction
    input_data = {
        'Property Size (sq ft)': property_size,
        f'Service Type_{service_type}': 1,
        f'Terrain Type_{terrain_type}': 1
    }

    # Fill missing columns with zeros
    for col in X.columns:
        if col not in input_data:
            input_data[col] = 0

    # Convert to DataFrame
    input_df = pd.DataFrame([input_data])

    # Reindex the input DataFrame to match the model's expected columns
    input_df = input_df.reindex(columns=X.columns, fill_value=0)

    # Make the base prediction
    base_quote = model.predict(input_df)[0]

    # Adjust the quote based on cost of living
    adjusted_quote = base_quote * cost_of_living

    # Calculate confidence interval (95%)
    lower_bound = adjusted_quote - 1.96 * std_dev
    upper_bound = adjusted_quote + 1.96 * std_dev

    # Display the adjusted quote
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
        model, _, mse, std_dev = train_model(custom_data)
        st.success("Model retrained with uploaded dataset!")
        st.write(f"Mean Squared Error: {mse:.2f}")
        st.write(f"Standard Deviation of Errors: {std_dev:.2f}")

# -----------------------------
# Stage 3: Visualize Data Page
# -----------------------------
elif menu == "Visualize Data 📊":
    st.title("Data Visualization")
    st.markdown("Explore the data used to train the model and see how it fits.")
    st.line_chart(df[['Property Size (sq ft)', 'Quote ($)']].set_index('Property Size (sq ft)'))
