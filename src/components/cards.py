import dash_bootstrap_components as dbc

# Specify card styling
card_style = {
    'borderRadius': '1rem',
    'overflow': 'hidden',
    'border': 'none',
    'boxShadow': 'none',
    'outline': 'none'
}

gdp_per_capita_card = dbc.Card(id='gdp-card', style=card_style)
population_card = dbc.Card(id='population-card', style=card_style)