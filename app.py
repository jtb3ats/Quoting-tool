# Import necessary libraries
import streamlit as st
import pandas as pd
import requests
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

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

# Function to train a model on the uploaded dataset
@st.cache
def train_model(data):
    data_encoded = pd.get_dummies(data, columns=['Service Type', 'Terrain Type'])
    X = data_encoded.drop('Quote ($)', axis=1)
    y = data_encoded['Quote ($)']
    model = LinearRegression()
    model.fit(X, y)
    return model, X

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
    terrain_type = st.selectbox("Select Terrain Type 🌄", ["Flat", "Sloped", "Mixed"])

    # Get location info
    if zip_code:
        city, state = get_location_info(zip_code)
        if city and state:
            st.write(f"Location: {city}, {state}")
        else:
            st.error("Invalid Zip Code. Please enter a valid US zip code.")

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
    model, X = train_model(df)

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

    input_df = pd.DataFrame([input_data])

    # Base quote prediction
    base_quote = model.predict(input_df)[0]

    # Adjust the quote based on the state's cost multiplier
    if zip_code:
        _, state = get_location_info(zip_code)
        adjusted_quote = base_quote * cost_multipliers.get(state, 1.0)
    else:
        adjusted_quote = base_quote

    # Display the adjusted quote
    if st.button("Get Quote 🔘"):
        st.success(f"Estimated Quote: ${adjusted_quote:.2f}")

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

        # Retrain the model with custom data
        model, _ = train_model(custom_data)
        st.success("Model retrained with uploaded dataset!")

# ----------------------------------------------
# Stage 3: Visualize Data Page
# ----------------------------------------------
elif menu == "Visualize Data 📊":
    st.title("Data Visualization")
    st.markdown("Explore the data used to train the model and see how it fits.")

    # Scatterplot of Property Size vs Quote
    st.markdown("### Property Size vs Quote")
    st.line_chart(df[['Property Size (sq ft)', 'Quote ($)']].set_index('Property Size (sq ft)'))
