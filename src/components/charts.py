import dash_vega_components as dvc

# World Map
world_map = dvc.Vega(id='world', opt={'actions': False}, spec={}, signalsToObserve=['select_region'])

# Pie Charts
energy_consumption_pie_chart = dvc.Vega(id='pie-chart', opt={'actions': False})
electricity_generation_pie_chart = dvc.Vega(id='electricity-production', opt={'actions': False})

# Bar Charts
electricity_access_bar_chart = dvc.Vega(id='bar-chart-electricity', opt={'actions': False}, style={'width': '100%'})
financial_flow_bar_chart = dvc.Vega(id='bar-chart-financial-flows', opt={'actions': False}, style={'width': '100%'})