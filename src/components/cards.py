import dash_bootstrap_components as dbc

card_style = {
    'borderRadius': '1rem',  # Rounded corners for the whole card
    'overflow': 'hidden',
    'border': 'none',
    'boxShadow': 'none',
    'outline': 'none'
}

gdp_per_capita_card = dbc.Card(id='gdp-card', style=card_style)
population_card = dbc.Card(id='population-card', style=card_style)