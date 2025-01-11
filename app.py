# Import necessary libraries
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# Set Streamlit page configuration
st.set_page_config(page_title="Smart Landscaping Quote Tool", layout="wide")

# -----------------------------
# Base Costs for Services
# -----------------------------
base_costs = {
    "Lawn Care": {"Small": 50, "Medium": 100, "Large": 200},
    "Tree Trimming": {"Small": 300, "Medium": 700, "Large": 1200},
    "Garden Maintenance": {"Small": 150, "Medium": 400, "Large": 800},
    "Irrigation Installation": {"Base": 2500},
    "Tree Removal": {"Base": 800},
    "Seasonal Services": {"Base": 200}
}

# -----------------------------
# Function to simulate job costs
# -----------------------------
def simulate_job_cost(zip_code, job_type, lot_size, complexity, special_requests):
    """Simulate job costs based on input parameters."""
    base_cost = base_costs[job_type][lot_size]
    complexity_multiplier = {"Flat": 1.0, "Sloped": 1.2, "Rocky": 1.3}
    adjusted_cost = base_cost * complexity_multiplier[complexity]

    if special_requests:
        adjusted_cost += 50

    lower_bound = adjusted_cost * 0.9
    upper_bound = adjusted_cost * 1.1

    return lower_bound, upper_bound

# Sidebar navigation
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
    job_type = st.selectbox("Select Job Type 🛠️", ["Lawn Care", "Tree Trimming", "Garden Maintenance", "Irrigation Installation", "Tree Removal", "Seasonal Services"])
    lot_size = st.selectbox("Select Lot Size 📏", ["Small", "Medium", "Large"])
    complexity = st.selectbox("Select Terrain Complexity 🌄", ["Flat", "Sloped", "Rocky"])
    special_requests = st.text_input("Special Requests (Optional)")

    if zip_code and job_type and lot_size and complexity:
        lower_bound, upper_bound = simulate_job_cost(zip_code, job_type, lot_size, complexity, special_requests)

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

        # Train the Random Forest model
        st.write("Training the model...")
        X = data[['ZIP Code', 'Job Type', 'Lot Size', 'Population Density', 'Median Home Value']]
        y = data['Actual Cost']
        model = RandomForestRegressor()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model.fit(X_train, y_train)

        # Predictions
        y_pred = model.predict(X_test)

        # Calculate performance metrics
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        # Display performance metrics
        st.success("Model retrained with uploaded data!")
        st.write(f"Mean Absolute Error: {mae:.2f}")
        st.write(f"R-Squared (R²): {r2:.2f}")

# -----------------------------
# Model Performance Page
# -----------------------------
elif menu == "Model Performance 📊":
    st.title("Model Performance")
    st.markdown("Track how your model is improving over time.")

    # Example performance metrics
    metrics = {
        "Mean Absolute Error": mae,
        "R-Squared": r2,
        "Number of Retrainings": 5  # Replace with a dynamic counter if needed
    }

    st.write(metrics)
