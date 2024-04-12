from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import altair as alt
import pandas as pd
import geopandas as gpd
import plotly.express as px

from callbacks import worldmap, piecharts, barcharts, cards
from data.data import raw_data, processed_data, world, gdf
from components.title import (
    title
)
from components.footer import (
    footer,
)
from components.filters import (
    metric_dropdown,
    year_slider,
    country_dropdown
)
from components.markdowns import (
    metric_dropdown_label,
    year_slider_label,
    country_dropdown_label
)
from components.filters import (
    metric_dropdown,
    year_slider,
    country_dropdown
)
from components.charts import (
    world_map,
    energy_consumption_pie_chart,
    electricity_generation_pie_chart,
    electricity_access_bar_chart,
    financial_flow_bar_chart,
)
from components.cards import (
    gdp_per_capita_card,
    population_card,
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

# Define the layout
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
    dbc.Row([
        dbc.Col(gdp_per_capita_card, width=6,),
        dbc.Col(population_card, width=6)
    ])
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

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

