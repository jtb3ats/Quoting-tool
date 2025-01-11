# Import necessary libraries
import pandas as pd
from sklearn.linear_model import LinearRegression
import streamlit as st

# Streamlit App Title
st.title("Property Quote Estimator")

# Data Preparation
data = {
    'Zip Code': [12345, 12346, 12347, 12348],
    'Property Size (sq ft)': [5000, 10000, 15000, 20000],
    'Quote ($)': [200, 400, 600, 800]
}

# Convert the data into a pandas DataFrame
df = pd.DataFrame(data)

# One-hot encoding for 'Zip Code' to handle categorical data
df_encoded = pd.get_dummies(df, columns=['Zip Code'])
X = df_encoded.drop('Quote ($)', axis=1)
y = df['Quote ($)']

# Model Training
model = LinearRegression()
model.fit(X, y)

# Streamlit Inputs
st.sidebar.header("Enter Property Details")

# Input Zip Code and Property Size
zip_code = st.sidebar.selectbox("Select Zip Code", df['Zip Code'].unique())
property_size = st.sidebar.number_input("Enter Property Size (sq ft)", min_value=1000, max_value=50000, step=1000)

# Ensure input DataFrame has the same columns as the model was trained on
input_data = {f'Zip Code_{zc}': 0 for zc in df['Zip Code'].unique()}  # Set all zip code columns to 0
input_data[f'Zip Code_{zip_code}'] = 1  # Set the selected zip code to 1
input_data['Property Size (sq ft)'] = property_size

# Convert to DataFrame
input_df = pd.DataFrame([input_data])

# Ensure the columns match exactly (fill missing columns with 0)
input_df = input_df.reindex(columns=X.columns, fill_value=0)

# Make the prediction
prediction = model.predict(input_df)[0]

# Display the result
st.write("### Estimated Quote:")
st.success(f"${prediction:.2f}")
