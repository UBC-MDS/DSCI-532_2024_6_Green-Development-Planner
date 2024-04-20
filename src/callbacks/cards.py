from dash import callback, Output, Input
import dash_bootstrap_components as dbc

from data.data import gdp_per_capita, population

# Callback to update card values based on selected country
@callback(
    [Output('gdp-card', 'children'),
     Output('population-card', 'children')],
    Input('entity-dropdown', 'value')
)
def update_card(selected_entity):

    gdp_per_capita_value = gdp_per_capita[gdp_per_capita['Entity'] == selected_entity]['gdp_per_capita'].iloc[0] 
    population_value = population[population["Entity"] == selected_entity]["pop_est"].iloc[0]

    # Specify card header styling 
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

    # Specify card body styling
    body_style = {
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

    gdp_card = [
        dbc.CardHeader(f'GDP per Capita (USD)', style=header_style),
        dbc.CardBody(f"{gdp_per_capita_value}", style=body_style)
    ]

    population_card = [
        dbc.CardHeader('Population', style=header_style),
        dbc.CardBody(f"{population_value}", style=body_style)
    ]

    return gdp_card, population_card