from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
from feature_scaling2 import preprocess_for_prediction  # Import your preprocessing logic
import datetime
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the trained model
MODEL_PATH = "random_forest_model2.pkl"
try:
    model = joblib.load(MODEL_PATH)
    logging.info(f"Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    logging.error(f"Error loading model: {str(e)}")
    raise

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Parse JSON input data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        # Define required fields
        required_fields = [
            "budget", "runtime", "release_date", "votes", "score", 
            "name", "rating", "genre", "director", "writer", 
            "star", "country", "company"
        ]

        # Validate required fields
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        # Extract and validate release_date
        try:
            release_date = datetime.datetime.strptime(data["release_date"], "%Y-%m-%d")
            release_date_str = release_date.strftime("%B %d, %Y")
            country = data["country"].strip()
            released = f"{release_date_str} ({country})"
            release_year = release_date.year
        except ValueError:
            return jsonify({"error": "Invalid release_date format. Use YYYY-MM-DD."}), 400

        # Parse numeric and categorical fields
        try:
            budget = float(data["budget"])
            runtime = float(data["runtime"])
            votes = int(data["votes"])
            score = float(data["score"])
        except ValueError:
            return jsonify({"error": "Invalid numeric value in input data."}), 400

        # Prepare categorical fields
        categorical_fields = {
            "genre": data["genre"].strip(),
            "rating": data["rating"].strip(),
            "name": data["name"].strip(),
            "director": data["director"].strip(),
            "writer": data["writer"].strip(),
            "star": data["star"].strip(),
            "country": data["country"].strip(),
            "company": data["company"].strip(),
        }

        # Create input DataFrame
        features = pd.DataFrame([{
            "name": categorical_fields["name"],
            "rating": categorical_fields["rating"],
            "genre": categorical_fields["genre"],
            "year": release_year,
            "released": released,
            "score": score,
            "votes": votes,
            "director": categorical_fields["director"],
            "writer": categorical_fields["writer"],
            "star": categorical_fields["star"],
            "country": categorical_fields["country"],
            "budget": budget,
            "company": categorical_fields["company"],
            "runtime": runtime
        }])

        logging.info("Input features successfully constructed.")

        # Preprocess features
        features_processed = preprocess_for_prediction(features)
        logging.info("Features successfully preprocessed.")

        # Make prediction
        prediction = model.predict(features_processed)

        # Reverse the log transformation to get the original-scale revenue
        box_office_revenue = np.expm1(prediction[0])  # np.expm1 reverses np.log1p
        box_office_revenue = round(box_office_revenue, 2)

        return jsonify({"box_office_revenue": box_office_revenue})

    except Exception as e:
        logging.error(f"Error during prediction: {str(e)}")
        return jsonify({"error": "An error occurred during prediction. Please try again."}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
