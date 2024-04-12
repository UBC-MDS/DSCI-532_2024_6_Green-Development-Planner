from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import altair as alt
import pandas as pd
import geopandas as gpd
import plotly.express as px

from data.data import raw_data, processed_data, world, gdf

header_style = {
    'fontWeight': 'bold',
    'color': '#245724',
    'backgroundColor': '#e6f5e6',
    'fontSize': '20px',
    'fontFamily': 'Helvetica',
    'padding': '15px',
    'textAlign': 'center',
    'border': 'none',
    'boxShadow': 'none',
    'outline': 'none'
}

body_style = {
    # 'fontWeight': 'bold',
    'color': '#f2fff2',
    'backgroundColor': '#245724',
    'fontSize': '22px',
    'fontFamily': 'Helvetica',
    'padding': '15px',
    'textAlign': 'center',
    'border': 'none',
    'boxShadow': 'none',
    'outline': 'none'
}

@callback(
    [Output('gdp-card', 'children'),
     Output('population-card', 'children')],
    Input('entity-dropdown', 'value')
)
def update_card(selected_entity):

    filtered_entity_data = processed_data[processed_data['Entity'] == selected_entity]
    gdp_per_capita = filtered_entity_data['gdp_per_capita'].iloc[0]   
    population = gdf[gdf["Entity"] == selected_entity]["pop_est"].iloc[-1]

    gdp_card = [
        dbc.CardHeader(f'GDP per Capita (USD)', style=header_style),
        dbc.CardBody(f"{gdp_per_capita: ,.2f}", style=body_style)
    ]

    population_card = [
        dbc.CardHeader('Population', style=header_style),
        dbc.CardBody(f"{population: ,.0f}", style=body_style)
    ]

    return gdp_card, population_card