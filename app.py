import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import json
from plotly.utils import PlotlyJSONEncoder

# Sample dataset (replace with your actual path)
df = pd.read_csv('D:\\Project 1 Credit Card Fraud Detection\\Data\\credit_card.csv')

# Helper function to filter data
def filter_data(fraud_class, amount_range):
    if fraud_class != 'all':
        filtered = df[df['Class'] == int(fraud_class)]
    else:
        filtered = df
    return filtered[(filtered['Amount'] >= amount_range[0]) & (filtered['Amount'] <= amount_range[1])]

# Save static JSON files
def save_visualizations():
    fraud_class = 'all'
    amount_range = [0, 10000]

    # Fraud Pie Chart
    filtered_data = filter_data(fraud_class, amount_range)
    fraud_count = filtered_data['Class'].value_counts()
    pie_chart = px.pie(
        names=fraud_count.index,
        values=fraud_count.values,
        title="Fraud vs Non-Fraud Transactions"
    )
    with open('fraud_pie_chart.json', 'w') as f:
        json.dump(pie_chart, f, cls=PlotlyJSONEncoder)

    # Heatmap
    correlation_matrix = filtered_data.iloc[:, 1:29].corr()
    heatmap = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        colorscale='Viridis'
    ))
    with open('heatmap.json', 'w') as f:
        json.dump(heatmap, f, cls=PlotlyJSONEncoder)

    # Scatter Plot
    scatter_plot = px.scatter(
        filtered_data, x='Time', y='Amount', color='Class',
        title="Time vs Amount for Fraud and Non-fraud Transactions"
    )
    with open('time_amount_scatter.json', 'w') as f:
        json.dump(scatter_plot, f, cls=PlotlyJSONEncoder)

    # 3D Scatter Plot
    scatter_3d_plot = px.scatter_3d(
        filtered_data, x='V1', y='V2', z='Amount', color='Class',
        title="3D Scatter Plot of V1, V2, and Amount"
    )
    with open('scatter_3d.json', 'w') as f:
        json.dump(scatter_3d_plot, f, cls=PlotlyJSONEncoder)

if __name__ == '__main__':
    save_visualizations()
