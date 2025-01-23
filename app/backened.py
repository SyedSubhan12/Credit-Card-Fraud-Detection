from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import logging
import os

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for specific origins
CORS(app, resources={r"*"})

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Path to the model file
MODEL_PATH = "D:/Project 1 Credit Card Fraud Detection/Credit-Card-Fraud-Detection/public2/random_forest_model.pkl"

# Load the model
model = None
try:
    assert os.path.exists(MODEL_PATH), f"Model file not found at {MODEL_PATH}"
    model = joblib.load(MODEL_PATH)
    logging.info("Model loaded successfully from %s", MODEL_PATH)
except Exception as e:
    logging.error("Error while loading model: %s", e)

# Expected number of features
EXPECTED_FEATURES = 30

# Define the prediction endpoint
@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        logging.error("Model not available. Please ensure the model file is correctly loaded.")
        return jsonify({"error": "Model not available."}), 500

    try:
        # Extract JSON data from the POST request
        data = request.json
        if not data or "data" not in data:
            logging.error("Invalid input: Missing 'data' key in request body.")
            return jsonify({"error": "Invalid input data format. Please provide a 'data' key."}), 400

        # Ensure the input is a list
        if not isinstance(data["data"], list):
            logging.error("Invalid input: 'data' key must contain a list of features.")
            return jsonify({"error": "Input data should be a list of features."}), 400

        # Check feature length
        if len(data["data"]) != EXPECTED_FEATURES:
            logging.error("Invalid input: Expected %d features, got %d", EXPECTED_FEATURES, len(data["data"]))
            return jsonify({"error": f"Expected {EXPECTED_FEATURES} features, but got {len(data['data'])}."}), 400

        # Convert input data to numpy array and reshape for prediction
        input_data = np.array(data["data"]).reshape(1, -1)  # Assuming input is a single sample
        logging.info("Received input data: %s", input_data)

        # Make prediction
        prediction = model.predict(input_data)
        prediction_label = "Fraud" if prediction[0] == 1 else "Not Fraud"
        logging.info("Prediction result: %s", prediction_label)

        # Return prediction result
        response = jsonify({"prediction": prediction_label})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 200

    except ValueError as ve:
        logging.error("ValueError during prediction: %s", ve)
        return jsonify({"error": str(ve)}), 400
    except KeyError as ke:
        logging.error("KeyError in input data: %s", ke)
        return jsonify({"error": f"Missing key in input: {ke}"}), 400
    except Exception as e:
        logging.error("Unexpected error: %s", e)
        return jsonify({"error": "An unexpected error occurred. Please try again."}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
