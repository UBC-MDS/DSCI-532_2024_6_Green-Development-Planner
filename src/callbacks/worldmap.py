from dash import callback, Output, Input, no_update
import altair as alt
import functools

from data.data import world, gdf

# Callback to update world map based on selection of metric and year
@callback(
    Output('world', 'spec'),
    [Input('variable', 'value'),
     Input('year_slider', 'value')]
)
@functools.lru_cache()
def create_chart(variable, year_slider):

    gdf_filtered = gdf[gdf['Year'] == year_slider]

    # Hover effect
    hover = alt.selection_point(
        fields=['Entity'], on='pointerover', empty=False
    )
    # Click effect
    click = alt.selection_point(
        fields=['Entity'], name='select_region', on='click'
    )

    def plot_chart(variable, color_scheme):
        return alt.Chart(gdf_filtered).mark_geoshape(
            stroke='#666666',
            strokeWidth=1
        ).project(
            'equalEarth'
        ).encode(
            color=alt.Color(variable, legend=alt.Legend(
                                            orient='none', 
                                            legendX=10, legendY=460, 
                                            direction='horizontal', 
                                            title=variable, 
                                            gradientLength=300, 
                                            labelLimit=500, 
                                            titleLimit=500
                                        )
            ).scale(scheme=color_scheme),
            tooltip=['Entity', variable],
            stroke=alt.condition(hover, alt.value('white'), alt.value('#666666')),
            order=alt.condition(hover, alt.value(1), alt.value(0))
        ).properties(
            width=600,
            height=500,
        ).add_params(
            hover,
            click
        )

    color_schemes = {
        'Electricity from fossil fuels (TWh)': 'browns',
        'Electricity from nuclear (TWh)': 'blues',
        'Financial flows to developing countries (US $)': 'purples'
    }

    # Use a default color scheme if the variable is not in the dictionary
    default_color_scheme = 'greens'

    # Determine the color scheme based on the variable
    selected_color_scheme = color_schemes.get(variable, default_color_scheme)

    # Create the chart with the selected color scheme
    non_missing_data = plot_chart(variable, selected_color_scheme)

    # Map background layer
    background_map = alt.Chart(world).mark_geoshape(color="lightgrey")

    # Return map data + background layer
    return((background_map + non_missing_data).to_dict())

# Callback to update the dropdown box based on the click on the map
@callback(
    Output('entity-dropdown', 'value'),
    [Input('world', 'signalData')] 
)
def update_dropdown(clicked_region):

    if clicked_region and 'Entity' in clicked_region['select_region']:
        entity = clicked_region['select_region']['Entity']

        # Check if the list is not empty
        if entity:  
            return entity[0]
        
        return no_update
    
    return no_update