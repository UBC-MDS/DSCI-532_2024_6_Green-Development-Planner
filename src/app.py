from dash import Dash, dcc, html, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import altair as alt
import dash_vega_components as dvc

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
    dbc.Row([
        dbc.Col(dcc.Graph(id='pie-chart')),
        dbc.Col(dvc.Vega(id='electricity-production')),
    ])
    ,
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

#callback to update electricity-production chart based on selected entity
@callback(
    Output('electricity-production', 'spec'),
    Input('entity-dropdown', 'value')
)

def update_arc_chart(selected_entity):
    # Filter the data for the selected entity
    filtered_data = processed_data[processed_data['Entity'] == selected_entity]
    
    # Sum up the electricity production share values for all the years for the entity
    # If the data is already averaged over the years, this step is not necessary
    green_electricity = filtered_data['Electricity from renewables (TWh)'].sum()
    nuclear_electricity = filtered_data['Electricity from nuclear (TWh)'].sum()
    fossil_electricity = filtered_data['Electricity from fossil fuels (TWh)'].sum()
    
    #store these number in a dataframe for altair to use
    source = pd.DataFrame({
        'Energy Source' : ['Renewables','Nuclear','Fossil Fuels'],
        'Value' : [green_electricity, nuclear_electricity, fossil_electricity]
        #'Value' : [4,50,6]
    })
    # Construct the arc chart figure using altair
    fig_electricity_production = alt.Chart(source).mark_arc(innerRadius=50).encode(
        theta = 'Value',
        color = 'Energy Source'
    ).properties(
        title = 'Electricity Generation'
    ).interactive().to_dict()

    return fig_electricity_production

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
