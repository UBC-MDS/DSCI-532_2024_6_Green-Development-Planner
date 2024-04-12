from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import altair as alt
import pandas as pd
import geopandas as gpd
import plotly.express as px

from data.data import raw_data, processed_data, world, gdf

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
        'Entity': [f'{selected_entity}', 'Average'],
        'Access to electricity (% of population)': [
            filtered_entity_data['Access to electricity (% of population)'].values[0],
            avg_access_to_electricity
        ]
    })

    bar_data_financial_flows = pd.DataFrame({
        'Entity': [f'{selected_entity}', 'Average'],
        'Financial flows to developing countries (US $)': [
            filtered_entity_data['Financial flows to developing countries (US $)'].values[0],
            avg_financial_flows
        ]
    })
    

    domain = [f'{selected_entity}','Average']
    range_ = ['#023020','#AFE1AF']

    fig_electricity = alt.Chart(bar_data_electricity).mark_bar().encode(
        x=alt.X('Access to electricity (% of population)', title='Access to Electricity (%)'),  # Change the title if needed
        y=alt.Y('Entity', title='Country'),
        color=alt.Color('Entity', legend=None).scale(domain=domain, range=range_),  # Move legend to top-left
        tooltip=["Entity", 'Access to electricity (% of population)'],
    ).properties(
        title=f"Access to Electricity - {selected_entity} vs Average",
        width=500
    ).to_dict()
    

    domain = [f'{selected_entity}','Average']
    range_ = ['#023020','#AFE1AF']

    fig_financial_flows = alt.Chart(bar_data_financial_flows).mark_bar().encode(
        x=alt.X('Financial flows to developing countries (US $)', title='Foreign Aid (US $)'),
        y=alt.Y('Entity', title='Country'),
        color=alt.Color('Entity', legend=None).scale(domain=domain, range=range_),  # Remove legend for color encoding
        tooltip=['Entity', 'Financial flows to developing countries (US $)'],
    ).properties(
        title=f"Recieved Foreign Aid - {selected_entity} vs Average",
        width=500
    ).to_dict()

    return fig_electricity, fig_financial_flows