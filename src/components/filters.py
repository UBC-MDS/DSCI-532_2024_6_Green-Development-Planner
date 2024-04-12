from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc

from data.data import metrics, gdf, processed_data

metric_dropdown = dcc.Dropdown(
    id='variable', 
    options=metrics, 
    value='Access to electricity (% of population)',
    placeholder="Select a metric",
)

year_slider = dcc.Slider(
    id='year_slider',
    min=gdf['Year'].min(),
    max=gdf['Year'].max(),
    value=gdf['Year'].max(),
    marks={str(year): str(year) for year in gdf['Year'].unique() if year % 5 == 0},
    step=20,
    updatemode="drag",
    tooltip={'placement': 'bottom', 'always_visible': True}
)

country_dropdown = dcc.Dropdown(
    id='entity-dropdown',
    options=[{'label': entity, 'value': entity} for entity in processed_data['Entity'].unique()],
    value=processed_data['Entity'].unique()[0],  # default value
)