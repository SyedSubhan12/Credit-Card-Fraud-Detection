from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import logging
import os

# Initialize Flask app
app = Flask(__name__)

# Enable CORS
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load the model
MODEL_PATH = "D:/Project 1 Credit Card Fraud Detection/Credit-Card-Fraud-Detection/Webapp/random_forest_model.pkl"
model = None
try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        logging.info("Model loaded successfully from %s", MODEL_PATH)
    else:
        logging.error("Model file not found at %s", MODEL_PATH)
except Exception as e:
    logging.error("Unexpected error while loading model: %s", e)

# Define the prediction endpoint
@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model not available."}), 500

    try:
        # Extract JSON data from the POST request
        data = request.json
        if not data or "data" not in data:
            return jsonify({"error": "Invalid input data format. Please provide a 'data' key."}), 400

        if not isinstance(data["data"], list):
            return jsonify({"error": "Input data should be a list of features."}), 400

        # Input data preprocessing
        input_data = np.array(data["data"]).reshape(1, -1)  # Assuming 1D array input
        logging.info("Received input data: %s", input_data)

        # Make prediction
        prediction = model.predict(input_data)
        prediction_label = "Fraud" if prediction[0] == 1 else "Not Fraud"
        logging.info("Prediction result: %s", prediction_label)

        # Return prediction result as JSON
        return jsonify({"prediction": prediction_label}), 200

    except ValueError as ve:
        logging.error("ValueError during prediction: %s", ve)
        return jsonify({"error": "Input data format mismatch. Please check your feature size and type."}), 400
    except Exception as e:
        logging.error("Error during prediction: %s", e)
        return jsonify({"error": "An error occurred during prediction."}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
