from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import altair as alt
import pandas as pd
import geopandas as gpd

world = gpd.read_file("data/preprocessed/world.shp")
world.crs = 'EPSG:4326'

gdf = gpd.read_file("data/preprocessed/preprocessed_data.shp", geometry="geometry")
gdf.crs = 'EPSG:4326'

print(world.info())

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

# Initiatlize the app
app = Dash()

metrics = [
    'Renewable energy share in the total final energy consumption (%)',
    'Access to electricity (% of population)',
    'Financial flows to developing countries (US $)',
    'Electricity from nuclear (TWh)',
    'Electricity from renewables (TWh)',
    'Electricity from fossil fuels (TWh)',
]

# Layout
app.layout = dbc.Container([
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

# Server side callbacks/reactivity
@callback(
    Output('world', 'spec'),
    [Input('variable', 'value'),
     Input('year_slider', 'value')]
)
def create_chart(variable, year_slider):

    gdf_filtered = gdf[gdf['Year'] == year_slider]
    non_missing_data = alt.Chart(gdf_filtered, width=600).mark_geoshape().encode(color=variable, tooltip=['Entity', variable])
    background_map = alt.Chart(world, width=600).mark_geoshape(color="lightgrey")

    return(
        (background_map + non_missing_data).to_dict()
    )

# Run the app/dashboard
app.run()
