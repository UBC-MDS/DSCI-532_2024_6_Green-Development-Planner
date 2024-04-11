from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import altair as alt
import pandas as pd
import geopandas as gpd
import plotly.express as px

raw_data = pd.read_csv("data/raw/global_data_sustainable_energy.csv")
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
server = app.server

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
    dcc.Markdown('**Select a Metric:**'),
    dcc.Dropdown(
        id='variable', 
        options=metrics, 
        value='Access to electricity (% of population)',
        placeholder="Select a metric",
        ),
    html.Br(),
    dcc.Markdown('**Select a Year:**'),
    dcc.Slider(
        id='year_slider',
        min=gdf['Year'].min(),
        max=gdf['Year'].max(),
        value=gdf['Year'].max(),
        marks={str(year): str(year) for year in gdf['Year'].unique() if year % 5 == 0},
        step=20,
        updatemode="drag",
        tooltip={'placement': 'bottom', 'always_visible': True}
    ),
    dvc.Vega(id='world', spec={}),
])

# Define the layout
right_layout = dbc.Container([
    dcc.Markdown('**Select a Country:**'),
    dcc.Dropdown(
        id='entity-dropdown',
        options=[{'label': entity, 'value': entity} for entity in processed_data['Entity'].unique()],
        value=processed_data['Entity'].unique()[0],  # default value
    ),
    html.Br(),
    dbc.Row([
        dbc.Col(dvc.Vega(id='pie-chart'), width=6),
        dbc.Col(dvc.Vega(id='electricity-production'), width=6),
    ]),
    html.Br(),
    dbc.Col(dvc.Vega(id='bar-chart-electricity', style={'width': '100%'})),
    html.Br(),
    dbc.Col(dvc.Vega(id='bar-chart-financial-flows', style={'width': '100%'})),
    html.Br(),
    dbc.Row([
        dbc.Col(dbc.Card(id='gdp-card'), width=6),
        dbc.Col(dbc.Card(id='population-card'), width=6)
    ])
])


description = html.P([
    "This dashboard offers a high-level overview of renewable energy metrics \
    across the globe and identifies developing countries with high potential \
    for green development.",
    html.Br(),  # Line break
    "Author: Ben Chen, Hayley Han, Ian MacCarthy, Joey Wu",
    html.Br(),  # Line break
    "Latest update/deployment: April 6, 2024",
    html.Br(),  # Line break
    html.A('GitHub URL', href='https://github.com/UBC-MDS/DSCI-532_2024_6_Green-Development-Planner', target='_blank')
])


app.layout = dbc.Container([
    dbc.CardBody('Green Development Planner', style={'font-family': 'Palatino, sans-serif', 'font-size': '3rem', 'color': 'green', 'text-align': 'center'}),
    dbc.Row([
        dbc.Col(left_layout, style={'width': '50%'}),
        dbc.Col(right_layout, style={'width': '50%'}),
    ]),

    dbc.Row([
        dbc.Col(
            description,
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
    [Output('gdp-card', 'children'),
     Output('population-card', 'children')],
    Input('entity-dropdown', 'value')
)
def update_card(selected_entity):

    filtered_entity_data = processed_data[processed_data['Entity'] == selected_entity]
    gdp_per_capita = filtered_entity_data['gdp_per_capita']   
    population = filtered_entity_data['gdp_per_capita']

    gdp_card = [
        dbc.CardHeader(f'GDP per Capita'),
        dbc.CardBody(gdp_per_capita)
    ]

    population_card = [
        dbc.CardHeader('Population'),
        dbc.CardBody(population)
    ]

    return gdp_card, population_card

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

