from dash import Dash, html
import dash_bootstrap_components as dbc

from callbacks import worldmap, piecharts, barcharts, cards

from components.title import title
from components.footer import footer
from components.filters import metric_dropdown, year_slider, country_dropdown
from components.markdowns import metric_dropdown_label, year_slider_label, country_dropdown_label
from components.filters import metric_dropdown, year_slider, country_dropdown
from components.charts import world_map, energy_consumption_pie_chart, electricity_generation_pie_chart, electricity_access_bar_chart, financial_flow_bar_chart
from components.cards import gdp_per_capita_card, population_card

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'src/assets/styles.css'])
server = app.server

# App layout of left side
left_layout = dbc.Container([
    dbc.Col(metric_dropdown_label, width=12),
    dbc.Col(metric_dropdown, width=12),
    html.Br(),
    dbc.Col(year_slider_label, width=12),
    dbc.Col(year_slider, width=12),
    dbc.Col(world_map, width=12),
])

# App layout of right side
right_layout = dbc.Container([
    dbc.Col(country_dropdown_label, width=12),
    dbc.Col(country_dropdown, width=12),
    html.Br(),
    dbc.Row([
        dbc.Col(energy_consumption_pie_chart, width=6),
        dbc.Col(electricity_generation_pie_chart, width=6),
    ]),
    html.Br(),
    dbc.Col(electricity_access_bar_chart, width=12),
    html.Br(),
    dbc.Col(financial_flow_bar_chart, width=12),
    html.Br(),
    dbc.Row([
        dbc.Col(gdp_per_capita_card, width=6),
        dbc.Col(population_card, width=6)
    ])
])

# App layout combining left and right side
app.layout = dbc.Container([
    dbc.Col(title, width=12),
    html.Br(),
    dbc.Row([
        dbc.Col(left_layout, width=6, style={"border": "2px solid #B8D9B8", "padding": "20px", "border-right": "none"}),
        dbc.Col(right_layout, width=6, style={"border": "2px solid #B8D9B8", "padding": "20px"}),
    ], align="stretch"),
    dbc.Col(footer, width=12)
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

