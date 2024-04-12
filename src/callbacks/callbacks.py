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

    domain = ['Renewables', "Other"]
    range_ = ['#4CBB17', '#C19A6B']

    pie_chart = alt.Chart(pie_data).mark_arc(innerRadius=50).encode(
        theta='value',
        color=alt.Color('category', legend=alt.Legend(title='Energy Source')).scale(domain=domain, range=range_),
        tooltip=['category', 'value']
    ).properties(
        title=f"Energy Consumption in {selected_entity}",
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

    domain = ['Renewables', "Fossil Fuels", "Nuclear"]
    range_ = ['#4CBB17', '#C19A6B', '#4682B4']

    fig_electricity_production = alt.Chart(source).mark_arc(innerRadius=50).encode(
        theta = 'Value',
        color = alt.Color('Energy Source', legend=alt.Legend(title='Energy Source')).scale(domain=domain, range=range_),
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