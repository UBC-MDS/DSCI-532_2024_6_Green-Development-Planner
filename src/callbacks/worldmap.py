from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import altair as alt
import pandas as pd
import geopandas as gpd
import plotly.express as px

from data.data import raw_data, processed_data, world, gdf

@callback(
    Output('world', 'spec'),
    [Input('variable', 'value'),
     Input('year_slider', 'value')]
)
def create_chart(variable, year_slider):

    gdf_filtered = gdf[gdf['Year'] == year_slider]

    # hover effect
    hover = alt.selection_point(
        fields=['Entity'], on='pointerover', empty=False
        )
    # click effect
    click = alt.selection_point(
        fields=['Entity'], name='select_region', on='click'
    )

    non_missing_data = alt.Chart(gdf_filtered, width=600, height=800).mark_geoshape(
        stroke='#666666',
        strokeWidth=1
    ).project(
        'equalEarth'
    ).encode(
        color=alt.Color(variable, 
                        legend=alt.Legend(orient='none', legendX=10, legendY=460, direction='horizontal',
                                          title=variable, gradientLength=300, 
                                          labelLimit=500, titleLimit=500)),
        # color=alt.Color(variable, legend=alt.Legend(orient='top-left')),
        tooltip=['Entity', variable],
        stroke=alt.condition(hover, alt.value('white'), alt.value('#666666')), 
        order=alt.condition(hover, alt.value(1), alt.value(0))
    ).add_params(
        hover,
        click
    )

    background_map = alt.Chart(world).mark_geoshape(color="lightgrey")

    return(
        (background_map + non_missing_data).properties(height=500).to_dict()
    )

# Callback to update the dropdown box based on the click on the map
@callback(
    Output('entity-dropdown', 'value'),
    [Input('world', 'signalData')] 
)
def update_dropdown(clicked_region):
    if clicked_region and 'Entity' in clicked_region['select_region']:
        return clicked_region['select_region']['Entity'][0]
    return processed_data['Entity'].unique()[0]