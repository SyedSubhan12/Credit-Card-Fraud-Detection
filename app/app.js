const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const path = require("path");
const fs = require("fs");
const { execSync } = require("child_process");

// Initialize Express app
const app = express();

// Enable CORS for all origins
app.use(cors());

// Configure body-parser to handle JSON request bodies
app.use(bodyParser.json());

// Path to the model file (make sure you save the model in a place accessible to this file)
const MODEL_PATH = "D:/Project 1 Credit Card Fraud Detection/Credit-Card-Fraud-Detection/Model/random_forest_model.pkl";

// Function to load the model
let model = null;
try {
    // Check if the model file exists
    if (fs.existsSync(MODEL_PATH)) {
        console.log("Model file found, loading...");
        // Load model using Python (since JavaScript doesn't have a native ML model loading tool)
        const loadModelCommand = `python -c "import joblib; model = joblib.load('${MODEL_PATH}'); print('Model loaded successfully')"`;
        const result = execSync(loadModelCommand).toString();
        console.log(result); // Log the successful loading
        model = true; // Mark the model as successfully loaded
    } else {
        console.error("Model file not found at", MODEL_PATH);
    }
} catch (err) {
    console.error("Error loading the model:", err);
}

// Expected number of features
const EXPECTED_FEATURES = 30;

// Prediction route
app.post("/predict", (req, res) => {
    if (!model) {
        return res.status(500).json({ error: "Model not available. Please ensure the model file is correctly loaded." });
    }

    try {
        const data = req.body;

        // Validate input data
        if (!data || !data.data) {
            return res.status(400).json({ error: "Invalid input: Missing 'data' key in request body." });
        }

        if (!Array.isArray(data.data)) {
            return res.status(400).json({ error: "'data' key must contain a list of features." });
        }

        if (data.data.length !== EXPECTED_FEATURES) {
            return res.status(400).json({
                error: `Expected ${EXPECTED_FEATURES} features, but got ${data.data.length}.`
            });
        }

        const input_data = data.data;
        console.log("Received input data:", input_data);

        // Make prediction via Python (if the model is in a separate Python environment)
        const inputString = input_data.join(","); // Convert to a comma-separated string for the Python script
        const predictCommand = `python -c "import joblib; model = joblib.load('${MODEL_PATH}'); input_data = [${inputString}]; prediction = model.predict([input_data]); print(prediction[0])"`;

        const prediction = execSync(predictCommand).toString().trim();
        const predictionLabel = prediction === "1" ? "Fraud" : "Not Fraud";
        console.log("Prediction result:", predictionLabel);

        // Respond with the prediction result
        res.status(200).json({ prediction: predictionLabel });
    } catch (err) {
        console.error("Error during prediction:", err);
        res.status(500).json({ error: "An unexpected error occurred. Please try again." });
    }
});

// Start the server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
