# Credit Card Fraud Detection Setup

## Project Overview
Credit card fraud detection is a critical problem faced by financial institutions, where identifying fraudulent transactions can prevent significant financial losses and improve customer trust. This project aims to build a machine learning model to detect fraudulent transactions in credit card data, addressing the challenges of class imbalance and maintaining high accuracy and recall.

## Dataset Description
**Source**: The dataset used for this project originates from [Kaggle's Credit Card Fraud Detection Dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud). It contains transactions made by European cardholders over two days in September 2013.

**Features**: The dataset has 31 features:
- **Time**: Seconds elapsed between this transaction and the first transaction in the dataset.
- **V1-V28**: Principal Component Analysis (PCA)-transformed features for confidentiality.
- **Amount**: Transaction amount.
- **Class**: Target variable (0 = legitimate, 1 = fraudulent).

**Preprocessing Steps**:
1. Normalization of the "Amount" feature to scale values between 0 and 1.
2. Splitting data into training and testing sets (80%-20%).
3. Addressing class imbalance using Synthetic Minority Oversampling Technique (SMOTE).

## Methodologies
### SMOTE (Synthetic Minority Oversampling Technique)
**Purpose**: To address the significant class imbalance (fraudulent transactions make up ~0.17% of the dataset).

**How it works**:
SMOTE generates synthetic examples of the minority class by interpolating between existing minority class samples, creating a balanced dataset for training.

**Advantages**:
- Reduces overfitting caused by oversampling with duplicates.
- Enhances the classifier’s ability to learn decision boundaries for minority classes.

### Random Classifier
**Purpose**: Establishes a baseline performance metric.

**Definition**: A random classifier assigns labels to transactions at random based on class distribution probabilities.

**Why Used**: Serves as a naive benchmark to compare the performance of advanced models.

### Model Development
- Models trained include Logistic Regression, Random Forest, and Gradient Boosted Trees.
- Performance evaluation metrics: Precision, Recall, F1 Score, ROC-AUC.

## Visualizations
### Class Distribution
Visualizes the imbalance in the dataset:
```python
sns.countplot(data=df, x='Class')
plt.title('Class Distribution')
plt.show()
```

### Correlation Matrix
Analyzes relationships between features:
```python
sns.heatmap(df.corr(), cmap='coolwarm', annot=False)
plt.title('Correlation Matrix')
plt.show()
```

### ROC Curve
Evaluates the model’s discriminatory ability:
```python
from sklearn.metrics import RocCurveDisplay
RocCurveDisplay.from_estimator(model, X_test, y_test)
plt.title('ROC Curve')
plt.show()
```

### Confusion Matrix
Provides detailed performance analysis:
```python
from sklearn.metrics import ConfusionMatrixDisplay
ConfusionMatrixDisplay.from_estimator(model, X_test, y_test, display_labels=['Legit', 'Fraud'])
plt.title('Confusion Matrix')
plt.show()
```

## Setup Instructions
### Dependencies
Install the following Python libraries:
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- imbalanced-learn

### Environment Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/credit-card-fraud-detection.git
   ```
2. Navigate to the project directory:
   ```bash
   cd credit-card-fraud-detection
   ```
3. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
### Training the Model
1. Run the preprocessing script:
   ```bash
   python preprocess.py
   ```
2. Train the model:
   ```bash
   python train_model.py
   ```

### Evaluating the Model
1. Evaluate the model performance:
   ```bash
   python evaluate_model.py
   ```
2. Generate visualizations:
   ```bash
   python generate_visualizations.py
   ```

This document provides a comprehensive guide to replicate and understand the Credit Card Fraud Detection project. For further details, please refer to the individual script documentation.
