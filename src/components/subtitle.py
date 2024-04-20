import dash_bootstrap_components as dbc
from dash import html

subtitle = dbc.CardBody([
    html.Br(),
    html.Div([
        html.P('This dashboard evaluates global potential for renewable energy development projects.', style={'margin-bottom': '0px'}),
        html.P('The map on the left shows a chosen metric for all countries, while the charts on the right show details for a chosen country.'),
    ])
],
    style={
        'font-family': 'Roboto, Arial, sans-serif',
        'font-size': '14px',
        'color': 'black',
        'text-align': 'center',
        'margin-left': '-11px',
    }
)
