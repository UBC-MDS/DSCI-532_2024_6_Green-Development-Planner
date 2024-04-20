from dash import callback, Output, Input
import altair as alt
import pandas as pd

from data.data import access_to_electricity, financial_flow

# Callbacks to update the bar charts based on selected country
@callback(
    [
        Output('bar-chart-electricity', 'spec'),
        Output('bar-chart-financial-flows', 'spec')
    ],
    Input('entity-dropdown', 'value')
)
def update_bar_charts(selected_entity):
    
    filtered_access_to_electricity = access_to_electricity[access_to_electricity['Entity'] == selected_entity]
    filtered_financial_flow = financial_flow[financial_flow['Entity'] == selected_entity]

    # Specify y-axis tick labels and colors for access to electricity bar chart
    domain = [f'{selected_entity}','Average']
    range_ = ['#023020','#AFE1AF']

    # Plot access to electricity bar chart
    access_to_electricity_bar_chart = alt.Chart(filtered_access_to_electricity).mark_bar().encode(
        x=alt.X('value', title='Access to Electricity (%)'),  # Change the title if needed
        y=alt.Y('category', title=None).sort([f'{selected_entity}', 'Average' ]),
        color=alt.Color('category', legend=None).scale(domain=domain, range=range_),  # Move legend to top-left
        tooltip=["category", 'value'],
    ).properties(
        title=f"Access to Electricity - {selected_entity} vs Average",
        width='container'
    ).to_dict()
    
    # Specify y-axis tick labels and colors for foreign aid bar chart
    domain = [f'{selected_entity}','Average']
    range_ = ['#023020','#AFE1AF']

    # Plot foreign aid bar chart
    financial_flows_bar_chart = alt.Chart(filtered_financial_flow).mark_bar().encode(
        x=alt.X('value', title='Foreign Aid (US $)'),
        y=alt.Y('category', title=None).sort([f'{selected_entity}', 'Average' ]),
        color=alt.Color('category', legend=None).scale(domain=domain, range=range_),  # Remove legend for color encoding
        tooltip=['category', 'value'],
    ).properties(
        title=f"Recieved Foreign Aid - {selected_entity} vs Average",
        width='container'
    ).to_dict()

    return access_to_electricity_bar_chart, financial_flows_bar_chart