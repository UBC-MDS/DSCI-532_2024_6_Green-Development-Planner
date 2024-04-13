from dash import callback, Output, Input
import altair as alt
import pandas as pd

from src.data.data import processed_data

# Callbacks to update the bar charts based on selected country
@callback(
    [
        Output('bar-chart-electricity', 'spec'),
        Output('bar-chart-financial-flows', 'spec')
    ],
    Input('entity-dropdown', 'value')
)
def update_bar_charts(selected_entity):
    
    filtered_entity_data = processed_data[processed_data['Entity'] == selected_entity]
    
    # Calculate the average for each metric of the country selected
    avg_access_to_electricity = processed_data['Access to electricity (% of population)'].mean()
    avg_financial_flows = processed_data['Financial flows to developing countries (US $)'].mean()

    # Selected country's metric
    selected_country_access_to_electricity = filtered_entity_data['Access to electricity (% of population)'].values[0]
    selected_country_financial_flows = filtered_entity_data['Financial flows to developing countries (US $)'].values[0]

    # If the selected values are missing
    if pd.isnull(selected_country_access_to_electricity):
        selected_country_access_to_electricity = 0
    if pd.isnull(selected_country_financial_flows):
        selected_country_financial_flows = 0

    # Construct access to electricity dataframe for plotting
    bar_data_electricity = pd.DataFrame({
        'Entity': [f'{selected_entity}', 'Average'],
        'Access to electricity (% of population)': [
            selected_country_access_to_electricity,
            avg_access_to_electricity
        ]
    })
    
    # Construct foreign aid dataframe for plotting
    bar_data_financial_flows = pd.DataFrame({
        'Entity': [f'{selected_entity}', 'Average'],
        'Financial flows to developing countries (US $)': [
            selected_country_financial_flows,
            avg_financial_flows
        ]
    })
    
    # Specify y-axis tick labels and colors for access to electricity bar chart
    domain = [f'{selected_entity}','Average']
    range_ = ['#023020','#AFE1AF']

    # Plot access to electricity bar chart
    access_to_electricity_bar_chart = alt.Chart(bar_data_electricity).mark_bar().encode(
        x=alt.X('Access to electricity (% of population)', title='Access to Electricity (%)'),  # Change the title if needed
        y=alt.Y('Entity', title='Country'),
        color=alt.Color('Entity', legend=None).scale(domain=domain, range=range_),  # Move legend to top-left
        tooltip=["Entity", 'Access to electricity (% of population)'],
    ).properties(
        title=f"Access to Electricity - {selected_entity} vs Average",
        width='container'
    ).to_dict()
    
    # Specify y-axis tick labels and colors for foreign aid bar chart
    domain = [f'{selected_entity}','Average']
    range_ = ['#023020','#AFE1AF']

    # Plot foreign aid bar chart
    financial_flows_bar_chart = alt.Chart(bar_data_financial_flows).mark_bar().encode(
        x=alt.X('Financial flows to developing countries (US $)', title='Foreign Aid (US $)'),
        y=alt.Y('Entity', title='Country'),
        color=alt.Color('Entity', legend=None).scale(domain=domain, range=range_),  # Remove legend for color encoding
        tooltip=['Entity', 'Financial flows to developing countries (US $)'],
    ).properties(
        title=f"Recieved Foreign Aid - {selected_entity} vs Average",
        width='container'
    ).to_dict()

    return access_to_electricity_bar_chart, financial_flows_bar_chart