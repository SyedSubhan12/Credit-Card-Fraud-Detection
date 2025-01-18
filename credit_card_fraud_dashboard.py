
# Import necessary libraries
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Initialize the app with a bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

data = pd.read_csv("D:/Project 1 Credit Card Fraud Detection/Data/credit_card.csv")

# Layout for the dashboard
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Credit Card Fraud Detection Dashboard", className="text-center mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id="class-filter",
                options=[
                    {"label": "All Classes", "value": "all"},
                    {"label": "Non-Fraud (Class 0)", "value": 0},
                    {"label": "Fraud (Class 1)", "value": 1}
                ],
                value="all",
                placeholder="Select Class",
                clearable=False
            )
        ], width=4),
        dbc.Col([
            dcc.RangeSlider(
                id="amount-filter",
                min=data['Amount'].min(),
                max=data['Amount'].max(),
                step=0.5,
                marks={
                    0: "0",
                    int(data['Amount'].max()): str(int(data['Amount'].max()))
                },
                value=[data['Amount'].min(), data['Amount'].max()]
            )
        ], width=8)
    ], className="mb-4"),
    dbc.Row([
        dbc.Col([dcc.Graph(id="amount-distribution")], width=6),
        dbc.Col([dcc.Graph(id="class-breakdown")], width=6)
    ]),
    dbc.Row([
        dbc.Col([dcc.Graph(id="time-trend")], width=12)
    ])
])

# Callbacks for interactivity
@app.callback(
    [Output("amount-distribution", "figure"),
     Output("class-breakdown", "figure"),
     Output("time-trend", "figure")],
    [Input("class-filter", "value"),
     Input("amount-filter", "value")]
)
def update_charts(selected_class, amount_range):
    filtered_data = data[
        (data['Amount'] >= amount_range[0]) & (data['Amount'] <= amount_range[1])
    ]
    if selected_class != "all":
        filtered_data = filtered_data[filtered_data['Class'] == selected_class]
    
    # Amount Distribution
    amount_fig = px.histogram(filtered_data, x="Amount", title="Amount Distribution")
    
    # Class Breakdown
    class_fig = px.pie(filtered_data, names="Class", title="Class Breakdown")
    
    # Time Trend
    time_fig = px.line(filtered_data, x="Time", y="Amount", title="Time vs Amount")
    
    return amount_fig, class_fig, time_fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
