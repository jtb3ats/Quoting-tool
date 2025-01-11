# Import necessary libraries
import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

# Set Streamlit page configuration
st.set_page_config(page_title="Instant Quote Tool", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Home 🏠", "Upload Data 📂", "Visualize Data 📊"])

# ----------------------------------------------
# Stage 1: Home Page (Input fields and Quote Prediction)
# ----------------------------------------------
if menu == "Home 🏠":
    st.title("Instant Quote Tool for Landscaping Services")
    st.markdown("Use this tool to get an instant quote based on property size, zip code, and type of service.")

    # Input fields
    zip_code = st.text_input("Enter Zip Code 🏙️", placeholder="E.g., 12345")
    property_size = st.number_input("Enter Property Size 📏 (in sq ft)", min_value=1000, max_value=50000, step=1000)
    service_type = st.selectbox("Select Service Type 🛠️", ["Lawn Care", "Tree Trimming", "Garden Maintenance"])

    # Predefined dataset (for demonstration purposes)
    data = {
        'Zip Code': [12345, 12346, 12347, 12348],
        'Property Size (sq ft)': [5000, 10000, 15000, 20000],
        'Service Type': ["Lawn Care", "Tree Trimming", "Garden Maintenance", "Lawn Care"],
        'Quote ($)': [200, 400, 600, 800]
    }
    df = pd.DataFrame(data)

    # One-hot encoding for categorical features
    df_encoded = pd.get_dummies(df, columns=['Zip Code', 'Service Type'])

    # Split data into features and target
    X = df_encoded.drop('Quote ($)', axis=1)
    y = df_encoded['Quote ($)']

    # Train a Linear Regression model
    model = LinearRegression()
    model.fit(X, y)

    # Create input DataFrame for prediction
    input_data = {
        f'Zip Code_{zip_code}': 1,
        'Property Size (sq ft)': property_size,
        f'Service Type_{service_type}': 1
    }

    # Fill missing columns with zeros
    for col in X.columns:
        if col not in input_data:
          
