# Import necessary libraries
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import time

# Set Streamlit page configuration
st.set_page_config(page_title="Smart Landscaping Quote Tool", layout="wide")

# -----------------------------
# Helper Functions
# -----------------------------
def simulate_job_costs(zip_code, job_type, lot_size, complexity, special_requests):
    """Simulate job costs based on input parameters."""
    # Base job costs (can be expanded)
    base_costs = {
        "Lawn Care": 100,
        "Tree Trimming": 250,
        "Garden Maintenance": 150
    }

    # Adjust costs based on lot size
    size_multiplier = {"Small": 1.0, "Medium": 1.2, "Large": 1.5}
    complexity_multiplier = {"Flat": 1.0, "Sloped": 1.2, "Rocky": 1.3}

    base_cost = base_costs[job_type]
    adjusted_cost = base_cost * size_multiplier[lot_size] * complexity_multiplier[complexity]

    # Add special request cost
    if special_requests:
        adjusted_cost += 50

    return adjusted_cost

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
    st.markdown("Get an instant quote based on property size, job type, and location.")

    # Input fields
    zip_code = st.text_input("Enter ZIP Code 🏙️", placeholder="E.g., 90210")
    job_type = st.selectbox("Select Job Type 🛠️", ["Lawn Care", "Tree Trimming", "Garden Maintenance"])
    lot_size = st.selectbox("Select Lot Size 📏", ["Small", "Medium", "Large"])
    complexity = st.selectbox("Select Terrain Complexity 🌄", ["Flat", "Sloped", "Rocky"])
    special_requests = st.text_input("Special Requests (Optional)")

    # Generate quote
    if st.button("Get Quote 🔘"):
        predicted_cost = simulate_job_costs(zip_code, job_type, lot_size, complexity, special_requests)
        lower_bound = predicted_cost * 0.9
        upper_bound = predicted_cost * 1.1
        st.success(f"Estimated Quote: ${lower_bound:.2f} - ${upper_bound:.2f}")

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

        # Train the Random Forest model
        st.write("Training the model...")
        X = data[['ZIP Code', 'Job Type', 'Lot Size', 'Population Density', 'Median Home Value']]
        y = data['Actual Cost']
        model = RandomForestRegressor()
        model.fit(X, y)

        st.success("Model retrained with uploaded data!")

# -----------------------------
# Model Performance Page
# -----------------------------
elif menu == "Model Performance 📊":
    st.title("Model Performance")
    st.markdown("Track the performance of your model over time.")

    # Example performance metrics
    metrics = {
        "Mean Absolute Error": 25.4,
        "R-Squared": 0.85,
        "Number of Retrainings": 5
    }

    st.write(metrics)
