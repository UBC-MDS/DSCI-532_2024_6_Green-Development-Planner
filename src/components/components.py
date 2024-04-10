from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc

from src.data.data import metrics, gdf, processed_data

metric_dropdown_label = dcc.Markdown('**Select a Metric:**')

metric_dropdown = dcc.Dropdown(
    id='variable', 
    options=metrics, 
    value='Access to electricity (% of population)',
    placeholder="Select a metric",
)

year_slider_label = dcc.Markdown('**Select a Year:**')

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

world_map = dvc.Vega(id='world', spec={})

country_dropdown_label = dcc.Markdown('**Select a Country:**')

country_dropdown = dcc.Dropdown(
    id='entity-dropdown',
    options=[{'label': entity, 'value': entity} for entity in processed_data['Entity'].unique()],
    value=processed_data['Entity'].unique()[0],  # default value
)

energy_consumption_pie_chart = dvc.Vega(id='pie-chart')
electricity_generation_pie_chart = dvc.Vega(id='electricity-production')

electricity_access_bar_chart = dvc.Vega(id='bar-chart-electricity', style={'width': '100%'})
financial_flow_bar_chart = dvc.Vega(id='bar-chart-financial-flows', style={'width': '100%'})

gdp_per_capita_line_chart = dvc.Vega(id='line-chart-gdp-per-capita', style={'width': '100%'})

footer = description = html.P([
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

title = dbc.CardBody('Green Development Planner', style={'font-family': 'Palatino, sans-serif', 'font-size': '3rem', 'color': 'green', 'text-align': 'center'})

