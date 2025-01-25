import pandas as pd
import joblib
import numpy as np
import datetime
from feature_scaling import preprocess_data

# Create sample data for testing
country = "United States"
release_date1 = "2021-12-17"
release_date = datetime.datetime.strptime(release_date1, "%Y-%m-%d")
release_date_str = release_date.strftime("%B %d, %Y")
released = f"{release_date_str} ({country.strip()})"
print (released)
test_data = pd.DataFrame({
    "name": ["The Call of the Wild"],
    "rating": ["PG"],
    "genre": ["Adventure"],
    "year": [2020],
    "released": ["February 21, 2020 (United States)"],
    "score": [6.8],
    "votes": [42000],  # Adjusted to match the example
    "director": ["Chris Sanders"],
    "writer": ["Michael Green"],
    "star": ["Harrison Ford"],
    "country": ["Canada"],
    "budget": [135000000.0],
    "company": ["20th Century Studios"],
    "runtime": [100.0]
})
df = pd.read_csv("E:\Box Office Revenue Prediction\Datasets\preparedDataset.csv")

# Call the preprocessing function
processed_data = preprocess_data(test_data)
print("Processed Data:\n", processed_data)

# Make prediction
model = joblib.load("../Models/random_forest_model.pkl")
prediction = model.predict(processed_data)

# Reverse the log transformation to get the original-scale revenue
box_office_revenue = np.expm1(prediction[0])  # np.expm1 reverses np.log1p
box_office_revenue = round(box_office_revenue, 2)
print(box_office_revenue)
       
