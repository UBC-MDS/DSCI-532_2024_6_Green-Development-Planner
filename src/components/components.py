from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc

from data.data import metrics, gdf, processed_data

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

world_map = dvc.Vega(id='world', opt={'actions': False}, spec={}, signalsToObserve=['select_region'])

country_dropdown_label = dcc.Markdown('**Select a Country:**')

country_dropdown = dcc.Dropdown(
    id='entity-dropdown',
    options=[{'label': entity, 'value': entity} for entity in processed_data['Entity'].unique()],
    value=processed_data['Entity'].unique()[0],  # default value
)

energy_consumption_pie_chart = dvc.Vega(id='pie-chart', opt={'actions': False})
electricity_generation_pie_chart = dvc.Vega(id='electricity-production', opt={'actions': False})

electricity_access_bar_chart = dvc.Vega(id='bar-chart-electricity', opt={'actions': False}, style={'width': '100%'})
financial_flow_bar_chart = dvc.Vega(id='bar-chart-financial-flows', opt={'actions': False}, style={'width': '100%'})

card_style = {
    'borderRadius': '1rem',  # Rounded corners for the whole card
    'overflow': 'hidden',
    'border': 'none',
    'boxShadow': 'none',
    'outline': 'none'
}

gdp_per_capita_card = dbc.Card(id='gdp-card', style=card_style)
population_card = dbc.Card(id='population-card', style=card_style)

footer = html.P([
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

title = dbc.CardBody('Green Development Planner',
                    style={
                        'font-family': 'Helvetica',
                        'font-size': '3rem',
                        'color': '#f2fff2',
                        'background-color':'#245724',
                        'text-align': 'center'
                    }
)

