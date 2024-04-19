import dash_bootstrap_components as dbc
from dash import html

subtitle = dbc.CardBody([
    html.Br(),
    html.H6('This dashboard evaluates global potential for renewable energy development projects.'),
    html.P('The map on the left shows a chosen metric for all countries, while the charts on the right show details for a chosen country.'),
                        ],
    style={
        'font-family': 'helvetica',
        'font-size': '16px',
        'color': '#f2fff2',
        'background-color':'#245724',
        'text-align': 'center',
        'width': '101.8%',
        'margin-left': '-11px'
    }
)
