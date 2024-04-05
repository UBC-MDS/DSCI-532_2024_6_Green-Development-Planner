from dash import Dash, dcc, html, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Load the dataset
processed_data = pd.read_csv("../data/processed_data.csv")

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout
app.layout = dbc.Container([
    dcc.Dropdown(
        id='entity-dropdown',
        options=[{'label': entity, 'value': entity} for entity in processed_data['Entity'].unique()],
        value=processed_data['Entity'].unique()[0],  # default value
    ),
    dcc.Graph(id='pie-chart'),
    dbc.Row([
        dbc.Col(dcc.Graph(id='bar-chart-electricity'), width=6),
        dbc.Col(dcc.Graph(id='bar-chart-financial-flows'), width=6),
    ]),
])

# Callback to update the pie chart based on selected entity
@callback(
    Output('pie-chart', 'figure'),
    Input('entity-dropdown', 'value')
)
def update_pie_chart(selected_entity):
    # Filter the data for the selected entity
    filtered_data = processed_data[processed_data['Entity'] == selected_entity]
    
    # Sum up the renewable energy share values for all the years for the entity
    # If the data is already averaged over the years, this step is not necessary
    renewable_energy_share = filtered_data['Renewable energy share in the total final energy consumption (%)'].sum()
    
    # Construct the pie chart figure using Plotly Express
    fig = px.pie(
        names=['Renewable Energy Share', 'Other'],
        values=[renewable_energy_share, 100 - renewable_energy_share],
        title=f"Renewable Energy Share in {selected_entity}"
    )
    
    # Return the figure to the output
    return fig

# Callbacks to update the bar charts based on selected entity
@callback(
    [
        Output('bar-chart-electricity', 'figure'),
        Output('bar-chart-financial-flows', 'figure')
    ],
    Input('entity-dropdown', 'value')
)
def update_bar_charts(selected_entity):
    # Filter the data for the selected entity
    filtered_entity_data = processed_data[processed_data['Entity'] == selected_entity]
    
    # Calculate the average for all entities for each metric
    avg_access_to_electricity = processed_data['Access to electricity (% of population)'].mean()
    avg_financial_flows = processed_data['Financial flows to developing countries (US $)'].mean()

    # Create the data for the bar chart, including the selected entity and the average
    bar_data_electricity = {
        'Entity': ['Selected Entity', 'Average'],
        'Access to electricity (% of population)': [
            filtered_entity_data['Access to electricity (% of population)'].values[0],
            avg_access_to_electricity
        ]
    }

    bar_data_financial_flows = {
        'Entity': ['Selected Entity', 'Average'],
        'Financial flows to developing countries (US $)': [
            filtered_entity_data['Financial flows to developing countries (US $)'].values[0],
            avg_financial_flows
        ]
    }
    
    # Create bar chart for "Access to electricity (% of population)"
    fig_electricity = px.bar(
        bar_data_electricity,
        x='Entity',
        y='Access to electricity (% of population)',
        title=f"Access to Electricity - {selected_entity} vs Average"
    )
    
    # Create bar chart for "Financial flows to developing countries (US $)"
    fig_financial_flows = px.bar(
        bar_data_financial_flows,
        x='Entity',
        y='Financial flows to developing countries (US $)',
        title=f"Financial Flows - {selected_entity} vs Average"
    )
    
    return fig_electricity, fig_financial_flows

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
