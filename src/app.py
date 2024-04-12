from dash import Dash, html
import dash_bootstrap_components as dbc

from src.callbacks import worldmap, piecharts, barcharts, cards

from src.components.title import title
from src.components.footer import footer
from src.components.filters import metric_dropdown, year_slider, country_dropdown
from src.components.markdowns import metric_dropdown_label, year_slider_label, country_dropdown_label
from src.components.filters import metric_dropdown, year_slider, country_dropdown
from src.components.charts import world_map, energy_consumption_pie_chart, electricity_generation_pie_chart, electricity_access_bar_chart, financial_flow_bar_chart
from src.components.cards import gdp_per_capita_card, population_card

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'src/assets/styles.css'])
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

# App layout of right side
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
        dbc.Col(gdp_per_capita_card),
        dbc.Col(population_card)
    ])
])

# App layout combining left and right side
app.layout = dbc.Container([
    title,
    dbc.Row([
        dbc.Col(left_layout),
        dbc.Col(right_layout),
    ]),
    dbc.Col(footer, width=12)
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

