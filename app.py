# Import necessary libraries
import os
os.system("pip install pillow==8.4.0")
import pandas as pd
from sklearn.linear_model import LinearRegression
import streamlit as st

# Data Preparation
data = {
    'Zip Code': [12345, 12346, 12347, 12348],
    'Property Size (sq ft)': [5000, 10000, 15000, 20000],
    'Quote ($)': [200, 400, 600, 800]
}

# Convert the data into a pandas DataFrame
df = pd.DataFrame(data)

# One-hot encoding for 'Zip Code' to handle categorical data
X = pd.get_dummies(df, columns=['Zip Code']) 

# Select features and target variable
X = X[['Zip Code_12345', 'Zip Code_12346', 'Zip Code_12347', 'Zip Code_12348', 'Property Size (sq ft)']]  
y = df['Quote ($)']

# Model Training, Create a Linear Regression model
model = LinearRegression()

# Train the model using the prepared data
model.fit(X, y)

# Input values for prediction
zip_code = 12348
property_size = 12000

# Create input data for prediction with one-hot encoded zip code
input_data = {'Zip Code_12345': 1, 'Zip Code_12346': 0, 'Zip Code_12347': 0, 'Zip Code_12348': 0, 'Property Size (sq ft)': property_size}
input_df = pd.DataFrame([input_data])

# Make the prediction
prediction = model.predict(input_df)

# Print the predicted quote
print(f"Estimated Quote: ${prediction[0]:.2f}")
