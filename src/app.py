from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import altair as alt
import pandas as pd
import geopandas as gpd
import plotly.express as px

from data.data import raw_data, processed_data, world, gdf
from components.components import (
    metric_dropdown_label,
    metric_dropdown,
    year_slider_label,
    year_slider,
    world_map,
    country_dropdown_label,
    country_dropdown,
    energy_consumption_pie_chart,
    electricity_generation_pie_chart,
    electricity_access_bar_chart,
    financial_flow_bar_chart,
    gdp_per_capita_line_chart,
    footer,
    title,
)

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# App layout of left side
left_layout = dbc.Container([
    metric_dropdown_label,
    metric_dropdown,
    html.Br(),
    year_slider_label,
    year_slider,
    world_map,
])

# App layout of right side
right_layout = dbc.Container([
    country_dropdown_label,
    country_dropdown,
    html.Br(),
    dbc.Row([
        dbc.Col(energy_consumption_pie_chart, width=6),
        dbc.Col(electricity_generation_pie_chart, width=6),
    ]),
    html.Br(),
    dbc.Col(electricity_access_bar_chart),
    html.Br(),
    dbc.Col(financial_flow_bar_chart),
    html.Br(),
    dbc.Col(gdp_per_capita_line_chart),
])

# App layout combining left and right side
app.layout = dbc.Container([
    title,
    dbc.Row([
        dbc.Col(left_layout, style={'width': '50%'}),
        dbc.Col(right_layout, style={'width': '50%'}),
    ]),
    dbc.Row([
        dbc.Col(
            footer,
            width=12,
            style={'font-size': '12px', 'color': '#333', 'margin-top': '20px', 'margin-bottom': '0', 'text-align': 'center', 'font-weight': 'bold'}
        )
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
    non_missing_data = alt.Chart(gdf_filtered, width=600, height=800).mark_geoshape().encode(
        color=alt.Color(variable, legend=alt.Legend(orient='top-left')),
        tooltip=['Entity', variable]
    )
    background_map = alt.Chart(world).mark_geoshape(color="lightgrey")

    return(
        (background_map + non_missing_data).properties(height=600).to_dict()
    )

# Callback to update the pie chart based on selected entity
@callback(
    Output('pie-chart', 'spec'),
    Input('entity-dropdown', 'value')
)
def update_pie_chart(selected_entity):
    # Filter the data for the selected entity
    filtered_data = processed_data[processed_data['Entity'] == selected_entity]
    
    # Sum up the renewable energy share values for all the years for the entity
    # If the data is already averaged over the years, this step is not necessary
    renewable_energy_share = filtered_data['Renewable energy share in the total final energy consumption (%)'].sum()
    
    pie_data = pd.DataFrame({
        'category': ['Renewables', 'Other'],
        'value': [renewable_energy_share, 100 - renewable_energy_share]
    })

    pie_chart = alt.Chart(pie_data).mark_arc(innerRadius=50).encode(
        theta='value',
        color=alt.Color('category', legend=alt.Legend(title='Category')),
        tooltip=['category', 'value']
    ).properties(
        title=f"Renewable Energy Share in {selected_entity}",
        width=150, height=150
    ).interactive().to_dict()
    
    # Return the Altair chart object
    return pie_chart 

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
        color = alt.Color('Energy Source', legend=alt.Legend(title='Energy Source')),
        tooltip=['Energy Source', 'Value']
    ).properties(
        title = f'Electricity Generation in {selected_entity}',
        width=150, height=150
    ).interactive().to_dict()

    return fig_electricity_production


# Callbacks to update the bar charts based on selected entity
@callback(
    [
        Output('bar-chart-electricity', 'spec'),
        Output('bar-chart-financial-flows', 'spec')
    ],
    Input('entity-dropdown', 'value')
)
def update_bar_charts(selected_entity):
    # Filter the data for the selected entity
    filtered_entity_data = processed_data[processed_data['Entity'] == selected_entity]
    
    # Calculate the average for all entities for each metric
    avg_access_to_electricity = processed_data['Access to electricity (% of population)'].mean()
    avg_financial_flows = processed_data['Financial flows to developing countries (US $)'].mean()

    bar_data_electricity = pd.DataFrame({
        'Entity': ['Selected Entity', 'Average'],
        'Access to electricity (% of population)': [
            filtered_entity_data['Access to electricity (% of population)'].values[0],
            avg_access_to_electricity
        ]
    })

    bar_data_financial_flows = pd.DataFrame({
        'Entity': ['Selected Entity', 'Average'],
        'Financial flows to developing countries (US $)': [
            filtered_entity_data['Financial flows to developing countries (US $)'].values[0],
            avg_financial_flows
        ]
    })
    
    fig_electricity = alt.Chart(bar_data_electricity).mark_bar().encode(
        x=alt.X('Access to electricity (% of population)', title='Access to Electricity (%)'),  # Change the title if needed
        y=alt.Y('Entity', title='Entity'),
        color=alt.Color('Entity', legend=None),  # Move legend to top-left
        tooltip=['Entity', 'Access to electricity (% of population)'],
    ).properties(
        title=f"Access to Electricity - {selected_entity} vs Average",
        width=500
    ).to_dict()
    

    fig_financial_flows = alt.Chart(bar_data_financial_flows).mark_bar().encode(
        x=alt.X('Financial flows to developing countries (US $)', title='Financial Flows (US $)'),
        y=alt.Y('Entity', title='Country'),
        color=alt.Color('Entity', legend=None),  # Remove legend for color encoding
        tooltip=['Entity', 'Financial flows to developing countries (US $)'],
    ).properties(
        title=f"Financial Flows - {selected_entity} vs Average",
        width=500
    ).to_dict()

    return fig_electricity, fig_financial_flows

@callback(
    Output('line-chart-gdp-per-capita', 'spec'),
    Input('entity-dropdown', 'value')
)
def update_pie_chart(selected_entity):

    raw_data['Year'] = pd.to_datetime(raw_data['Year'], format='%Y')
    filtered_entity_data = raw_data[raw_data['Entity'] == selected_entity]

    gdp_per_capita_line_plot = alt.Chart(filtered_entity_data).mark_line().encode(
        x=alt.X('Year:T', title='Year'),  # Assuming 'Year' column is datetime, adjust if necessary
        y=alt.Y('gdp_per_capita', title='GDP per Capita'),
        tooltip=['Year:T', 'gdp_per_capita']
    ).properties(
        title=f"GDP per Capita over Time for {selected_entity}",
        width=550, height=200
    ).to_dict()

    return gdp_per_capita_line_plot

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)

