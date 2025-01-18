from train_model import X_test_scaled, rf
import pandas as pd
#  Test with a single test sample
single_test_sample = X_test_scaled[0].reshape(1, -1)  # Select the first sample
single_test_prediction = rf.predict(single_test_sample)
single_test_probability = rf.predict_proba(single_test_sample)[:, 1]

# Print the prediction and probability
print(f"Prediction for the single test sample: {single_test_prediction[0]}")
print(f"Probability of fraud for the single test sample: {single_test_probability[0]:.4f}")

# Save the result to a file
result = pd.DataFrame({
    'Prediction': [single_test_prediction[0]],
    'Probability': [single_test_probability[0]]
})

# Save to CSV file
result.to_csv('/Model/single_test_prediction.csv', index=False)

print("Prediction saved to single_test_prediction.csv")

import joblib
# Save the trained RandomForest model to a file
model_filename = '/Model/random_forest_model.pkl'
joblib.dump(rf, model_filename)

print(f"Model saved to {model_filename}")