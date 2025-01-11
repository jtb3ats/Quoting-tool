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
    input_data = {f'Zip Code_{zip_code}': 1, 'Property Size (sq ft)': property_size}
    for service in df['Service Type'].unique():
        input_data[f'Service Type_{service}'] = 1 if service == service_type else 0

    # Fill missing columns with zeros
    for col in X.columns:
        if col not in input_data:
            input_data[col] = 0

    input_df = pd.DataFrame([input_data])

    # Make a prediction
    if st.button("Get Quote 🔘"):
        prediction = model.predict(input_df)[0]
        st.success(f"Estimated Quote: ${prediction:.2f}")

# ----------------------------------------------
# Stage 2: Upload Data Page
# ----------------------------------------------
elif menu == "Upload Data 📂":
    st.title("Upload Your Dataset")
    st.markdown("Upload your own CSV file to retrain the model with your business-specific data.")

    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        custom_data = pd.read_csv(uploaded_file)
        st.write("Uploaded Dataset:")
        st.dataframe(custom_data)

        # One-hot encoding for custom dataset
        custom_data_encoded = pd.get_dummies(custom_data, columns=['Zip Code', 'Service Type'])

        # Split data into features and target
        X_custom = custom_data_encoded.drop('Quote ($)', axis=1)
        y_custom = custom_data_encoded['Quote ($)']

        # Retrain the model with custom data
        model.fit(X_custom, y_custom)
        st.success("Model retrained with uploaded dataset!")

# ----------------------------------------------
# Stage 3: Visualize Data Page
# ----------------------------------------------
elif menu == "Visualize Data 📊":
    st.title("Data Visualization")
    st.markdown("Explore the data used to train the model and see how it fits.")

    # Scatterplot of Property Size vs Quote
    st.markdown("### Property Size vs Quote")
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x="Property Size (sq ft)", y="Quote ($)", hue="Service Type", ax=ax)
    st.pyplot(fig)

    # Predicted vs Actual Quotes (if custom data was uploaded)
    if uploaded_file is not None:
        st.markdown("### Predicted vs Actual Quotes")
        y_pred = model.predict(X_custom)
        fig, ax = plt.subplots()
        sns.scatterplot(x=y_custom, y=y_pred, ax=ax)
        ax.set_xlabel("Actual Quotes")
        ax.set_ylabel("Predicted Quotes")
        st.pyplot(fig)
