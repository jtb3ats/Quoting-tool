import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import requests

# Set Streamlit page configuration
st.set_page_config(page_title="Smart Landscaping Quote Tool", layout="wide")

# -----------------------------
# Function to get location-based pricing
# -----------------------------
def get_location_multiplier(zip_code):
    """Fetch location-based pricing multiplier using ZIP code."""
    # Placeholder function: Replace with actual API call or database lookup
    # For demonstration, returning a dummy multiplier
    return 1.0  # Default multiplier

# -----------------------------
# Base Costs for Services
# -----------------------------
base_costs = {
    "Lawn Care": {
        "Up to 5,000 sq ft": 50,
        "5,000 - 10,000 sq ft": 100,
        "Over 10,000 sq ft": 200
    },
    "Tree Trimming": {
        "1-2 Trees": 300,
        "3-5 Trees": 700,
        "6+ Trees": 1200
    },
    "Garden Maintenance": {
        "Up to 1,000 sq ft": 150,
        "1,000 - 5,000 sq ft": 400,
        "Over 5,000 sq ft": 800
    },
    "Irrigation Installation": {
        "Base Cost": 2500
    },
    "Tree Removal": {
        "Small Tree": 300,
        "Medium Tree": 800,
        "Large Tree": 1500
    },
    "Seasonal Services": {
        "Small Job": 100,
        "Medium Job": 250,
        "Large Job": 400
    },
    "Snow Clearing": {
        "Up to 1,000 sq ft": 100,
        "1,000 - 5,000 sq ft": 250,
        "Over 5,000 sq ft": 400
    }
}

# -----------------------------
# Function to simulate job costs
# -----------------------------
def simulate_job_cost(zip_code, job_type, size_category, complexity, special_requests):
    """Simulate job costs based on input parameters."""
    # Fetch location-based multiplier
    location_multiplier = get_location_multiplier(zip_code)

    # Check if the job type exists in base_costs
    if job_type not in base_costs:
        st.warning(f"Job type '{job_type}' is not recognized. Please select a valid job type.")
        return 0, 0

    # Get the base cost based on size category
    base_cost = base_costs[job_type].get(size_category, 0)

    # Adjust for terrain complexity (if applicable)
    complexity_multiplier = {"Flat": 1.0, "Sloped": 1.2, "Rocky": 1.3}
    adjusted_cost = base_cost * complexity_multiplier.get(complexity, 1.0)

    # Apply location multiplier
    adjusted_cost *= location_multiplier

    # Add special request cost
    if special_requests:
        adjusted_cost += 50

    # Return a confidence interval
    lower_bound = adjusted_cost * 0.9
    upper_bound = adjusted_cost * 1.1

    return lower_bound, upper_bound

# -----------------------------
# Sidebar navigation
# -----------------------------
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Home 🏠", "Upload Data 📂", "Model Performance 📊"])

# -----------------------------
# Home Page
# -----------------------------
if menu == "Home 🏠":
    st.title("Smart Landscaping Quote Tool")
    st.markdown("Get instant quotes for landscaping services based on your inputs.")

    # Input fields
    zip_code = st.text_input("Enter ZIP Code 🏙️", placeholder="E.g., 90210")

    # Ensure ZIP code is treated as a string and properly formatted
    if zip_code:
        zip_code = zip_code.zfill(5)  # This ensures the ZIP code has leading zeros

    job_type = st.selectbox("Select Job Type 🛠️", [
        "Lawn Care", "Tree Trimming", "Garden Maintenance",
        "Irrigation Installation", "Tree Removal", "Seasonal Services", "Snow Clearing"
    ])

    # Size category options based on job type
    if job_type == "Lawn Care":
        size_category = st.selectbox("Select Lawn Size 📏", ["Up to 5,000 sq ft", "5,000 - 10,000 sq ft", "Over 10,000 sq ft"])
    elif job_type == "Tree Trimming":
        size_category = st.selectbox("Select Number of Trees 🌳", ["1-2 Trees", "3-5 Trees", "6+ Trees"])
    elif job_type == "Garden Maintenance":
        size_category = st.selectbox("Select Garden Size 🌷", ["Up to 1,000 sq ft", "1,000 - 5,000 sq ft", "Over 5,000 sq ft"])
    elif job_type == "Irrigation Installation":
        size_category = st.selectbox("Select Installation Type 💧", ["Base Cost"])
    elif job_type == "Tree Removal":
        size_category = st.selectbox("Select Tree Size 🌲", ["Small Tree", "Medium Tree", "Large Tree"])
    elif job_type == "Seasonal Services":
        size_category = st.selectbox("Select Job Size 🍂", ["Small Job", "Medium Job", "Large Job"])
    elif job_type == "Snow Clearing":
        size_category = st.selectbox("Select Area Size ❄️", ["Up to 1,000 sq ft", "1,000 - 5,000 sq ft", "Over 5,000 sq ft"])
    else:
        size_category = st.selectbox("Select Size Category 📏", ["Unknown"])

    complexity = st.selectbox("Select Terrain Complexity 🌄", ["Flat", "Sloped", "Rocky"])
    special_requests = st.text_input("Special Requests (Optional)")

    # Dynamic quote prediction
    if zip_code and job_type and size_category and complexity:
        lower_bound, upper_bound = simulate_job_cost(zip_code, job_type, size_category, complexity, special_requests)

        st.markdown(f"""
        <div style="background-color:#f9f9f9;padding:20px;border-radius:10px;">
            <h3>Estimated Quote 💰</h3>
            <p><strong>Range:</strong> ${lower_bound:.2f} - ${upper_bound:.2f}</p>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------
# Upload Data Page
# -----------------------------
elif menu == "Upload Data 📂":
    st.title("Upload Your Job Data for Model Training")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        # Load the uploaded CSV
        data = pd.read_csv(uploaded_file)
        st.write("Uploaded Dataset:")
        st.dataframe(data)

        # Feature Expansion: Add more features for training the model
        # This section can be expanded based on further requirements

# -----------------------------
# Model Performance Page
# -----------------------------
elif menu == "Model Performance 📊":
    st.title("Model Performance Overview")
    st.markdown("This page will display the model's performance metrics such as R2, MAE, and more based on the dataset.")
    # Implement model training and performance metrics here if necessary
