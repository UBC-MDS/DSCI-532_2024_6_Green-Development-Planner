from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import altair as alt
import pandas as pd
import geopandas as gpd
import plotly.express as px

processed_data = pd.read_csv("data/preprocessed/processed_data.csv")

world = gpd.read_file("data/preprocessed/world.shp")
world.crs = 'EPSG:4326'

gdf = gpd.read_file("data/preprocessed/preprocessed_data.shp", geometry="geometry")
gdf.crs = 'EPSG:4326'

rename_dict = {
    'Renewable': 'Renewable energy share in the total final energy consumption (%)',
    'Access to': 'Access to electricity (% of population)',
    'Financial': 'Financial flows to developing countries (US $)',
    'Electricit': 'Electricity from nuclear (TWh)',
    'Electric_1': 'Electricity from renewables (TWh)',
    'Electric_2': 'Electricity from fossil fuels (TWh)',
    'gdp_per_ca': 'gdp_per_capita_y'
}
gdf = gdf.rename(columns=rename_dict)


# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

metrics = [
    'Renewable energy share in the total final energy consumption (%)',
    'Access to electricity (% of population)',
    'Financial flows to developing countries (US $)',
    'Electricity from nuclear (TWh)',
    'Electricity from renewables (TWh)',
    'Electricity from fossil fuels (TWh)',
]

# Layout
left_layout = dbc.Container([
    dvc.Vega(id='world', spec={}),
    dcc.Slider(
        id='year_slider',
        min=gdf['Year'].min(),
        max=gdf['Year'].max(),
        value=gdf['Year'].max(),
        marks={str(year): str(year) for year in gdf['Year'].unique()},
        step=None,
        updatemode="drag"
    ),
    dcc.Dropdown(id='variable', options=metrics, value='Renewable energy share in the total final energy consumption (%)'),
])

# Define the layout
right_layout = dbc.Container([
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

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(left_layout, style={'height': '100%'}, width=6),
        dbc.Col(right_layout, style={'height': '100%'}, width=6),
    ])
])

# Server side callbacks/reactivity
@callback(
    Output('world', 'spec'),
    [Input('variable', 'value'),
     Input('year_slider', 'value')]
)
def create_chart(variable, year_slider):

    gdf_filtered = gdf[gdf['Year'] == year_slider]
    non_missing_data = alt.Chart(gdf_filtered, width=600, height=800).mark_geoshape().encode(color=variable, tooltip=['Entity', variable])
    background_map = alt.Chart(world, width=600, height=800).mark_geoshape(color="lightgrey")

    return(
        (background_map + non_missing_data).to_dict()
    )

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
