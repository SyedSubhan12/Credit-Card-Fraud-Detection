import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# Load the dataset
def load_data(file_path):
    """Loads the dataset into a pandas DataFrame."""
    return pd.read_csv(file_path)

# Time series plot for key columns over time
def plot_time_series(df, columns, output_path):
    """Generates interactive time series line plots for the selected columns."""
    for col in columns:
        if col in df.columns:
            fig = px.line(df, x='Time', y=col, title=f"Time Series of {col}")
            fig.write_html(f"{output_path}/{col}_time_series.html")
        else:
            print(f"Column '{col}' not found in the dataset.")

# Correlation heatmap
# Correlation heatmap
def plot_correlation_heatmap(df, numerical_columns, output_path):
    """Generates an interactive correlation heatmap for numerical columns."""
    available_cols = [col for col in numerical_columns if col in df.columns]
    if available_cols:
        corr = df[available_cols].corr()
        fig = px.imshow(corr, text_auto=True, color_continuous_scale='Viridis', title="Correlation Heatmap")
        fig.write_html(f"{output_path}/correlation_heatmap.html")
    else:
        print("No valid numerical columns for correlation heatmap.")

# Distribution of numerical columns
def plot_numerical_distributions(df, numerical_columns, output_path):
    """Plots interactive histograms for numerical columns."""
    for col in numerical_columns:
        if col in df.columns:
            fig = px.histogram(df, x=col, nbins=30, title=f"Distribution of {col}")
            fig.write_html(f"{output_path}/{col}_distribution.html")
        else:
            print(f"Column '{col}' not found in the dataset.")

# Pair plot for selected columns
def plot_pair_plot(df, columns, output_path):
    """Generates an interactive pair plot for selected columns."""
    available_cols = [col for col in columns if col in df.columns]
    if available_cols:
        fig = px.scatter_matrix(df, dimensions=available_cols, title="Pair Plot")
        fig.write_html(f"{output_path}/pair_plot.html")
    else:
        print(f"No valid columns for pair plot.")

# Box plot for numerical columns
def plot_box_plot(df, numerical_columns, output_path):
    """Generates box plots for numerical columns to detect outliers."""
    for col in numerical_columns:
        if col in df.columns:
            fig = px.box(df, y=col, title=f"Box Plot of {col}")
            fig.write_html(f"{output_path}/{col}_box_plot.html")
        else:
            print(f"Column '{col}' not found in the dataset.")

# Time series anomaly detection (Optional)
def plot_anomaly_detection(df, column, output_path):
    """Optional: Detect and plot anomalies in a time series column."""
    if column in df.columns:
        # Calculate rolling mean and standard deviation for anomaly detection
        rolling_mean = df[column].rolling(window=50).mean()
        rolling_std = df[column].rolling(window=50).std()
        upper_bound = rolling_mean + (rolling_std * 2)
        lower_bound = rolling_mean - (rolling_std * 2)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Time'], y=df[column], mode='lines', name=column))
        fig.add_trace(go.Scatter(x=df['Time'], y=rolling_mean, mode='lines', name='Rolling Mean', line=dict(dash='dash')))
        fig.add_trace(go.Scatter(x=df['Time'], y=upper_bound, mode='lines', name='Upper Bound', line=dict(dash='dot')))
        fig.add_trace(go.Scatter(x=df['Time'], y=lower_bound, mode='lines', name='Lower Bound', line=dict(dash='dot')))
        
        fig.update_layout(title=f"Anomaly Detection in {column}", xaxis_title="Time", yaxis_title=column)
        fig.write_html(f"{output_path}/{column}_anomaly_detection.html")
    else:
        print(f"Column '{column}' not found in the dataset.")

# Visualize the class distribution
def plot_class_distribution(df, output_path):
    """Creates a pie chart to show the distribution of Class (fraud vs. non-fraud)."""
    if 'Class' in df.columns:
        fig = px.pie(df, names='Class', title="Class Distribution (Fraud vs Non-Fraud)")
        fig.write_html(f"{output_path}/class_distribution.html")
    else:
        print(f"Column 'Class' not found in the dataset.")

# Main function to execute the visualization pipeline
def main(file_path, output_path):
    """Executes the visualization pipeline for the provided dataset."""
    df = load_data(file_path)

    # Time Series Plot for Columns V1, V2, ..., V28
    time_series_columns = ['V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10']  # Specify your desired columns
    plot_time_series(df, time_series_columns, output_path)

    # Correlation heatmap for numerical columns
    numerical_columns = ['V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'Amount']  # Adjust as needed
    plot_correlation_heatmap(df, numerical_columns, output_path)

    # Distribution of numerical columns
    plot_numerical_distributions(df, numerical_columns, output_path)

    # Pair plot for selected numerical columns
    selected_columns = ['V1', 'V2', 'Amount']  # Adjust as needed
    plot_pair_plot(df, selected_columns, output_path)

    # Box plot for numerical columns
    plot_box_plot(df, numerical_columns, output_path)

    # Optional: Anomaly detection for the 'Amount' column
    plot_anomaly_detection(df, 'Amount', output_path)

    # Class distribution visualization (fraud vs non-fraud)
    plot_class_distribution(df, output_path)

    print("Analysis completed. All plots saved to the output directory, including interactive visualizations.")

# Example usage
file_path = 'D:/Project 1 Credit Card Fraud Detection/Data/credit_card.csv'  # Replace with your dataset file path
output_path = 'Visualization'  # Replace with your desired output directory

import os
if not os.path.exists(output_path):
    os.makedirs(output_path)

main(file_path, output_path)
