# disaster_prediction_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from joblib import dump

# Load historical data
data = pd.read_csv('dataset.csv')

# Handle missing values
data = data.dropna()  # This drops rows with any missing values; adjust as needed

# Label encode the target variable
label_encoder = LabelEncoder()
labels = label_encoder.fit_transform(data['Disaster'])  # Adjust this line based on your target variable

# Features: Temperature, Rainfall, Wind_Speed
features = data[['Temperature', 'Rainfall', 'Wind_Speed']]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Save the trained model
dump(model, 'disaster_prediction_model.joblib')
