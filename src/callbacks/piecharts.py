from dash import callback, Output, Input
import altair as alt
import pandas as pd

from data.data import processed_data

# Callback to update the energy consumption pie chart based on selected country
@callback(
    Output('pie-chart', 'spec'),
    Input('entity-dropdown', 'value')
)
def update_energy_consumption_chart(selected_entity):

    filtered_data = processed_data[processed_data['Entity'] == selected_entity]
    
    # Sum up the renewable energy share values for all years in the dataset
    renewable_energy_share = filtered_data['Renewable energy share in the total final energy consumption (%)'].sum()
    
    pie_data = pd.DataFrame({
        'category': ['Renewables', 'Other'],
        'value': [renewable_energy_share, 100 - renewable_energy_share]
    })

    # Specify legend titles and colors
    domain = ['Renewables', "Other"]
    range_ = ['#4CBB17', '#C19A6B']

    # Plot pie chart
    energy_consumption_pie_chart = alt.Chart(pie_data).mark_arc(innerRadius=50).encode(
        theta='value',
        color=alt.Color('category', legend=alt.Legend(title='Energy Source')).scale(domain=domain, range=range_),
        tooltip=['category', 'value']
    ).properties(
        title=f"Energy Consumption in {selected_entity}",
        width=150, height=150
    ).interactive().to_dict()
    
    return energy_consumption_pie_chart

#callback to update electricity generation pie chart based on selected country
@callback(
    Output('electricity-production', 'spec'),
    Input('entity-dropdown', 'value')
)
def update_electricty_generation_chart(selected_entity):

    filtered_data = processed_data[processed_data['Entity'] == selected_entity]
    
    # Sum up the electricity production share values for all the years for the entity
    green_electricity = filtered_data['Electricity from renewables (TWh)'].sum()
    nuclear_electricity = filtered_data['Electricity from nuclear (TWh)'].sum()
    fossil_electricity = filtered_data['Electricity from fossil fuels (TWh)'].sum()
    
    #store these number in a dataframe for altair to use
    source = pd.DataFrame({
        'Energy Source' : ['Renewables','Nuclear','Fossil Fuels'],
        'Value' : [green_electricity, nuclear_electricity, fossil_electricity]
    })

    # Specify legend titles and colors
    domain = ['Renewables', "Fossil Fuels", "Nuclear"]
    range_ = ['#4CBB17', '#C19A6B', '#4682B4']

    # Plot pie chart
    electricity_consumption_pie_chart = alt.Chart(source).mark_arc(innerRadius=50).encode(
        theta = 'Value',
        color = alt.Color('Energy Source', legend=alt.Legend(title='Energy Source')).scale(domain=domain, range=range_),
        tooltip=['Energy Source', 'Value']
    ).properties(
        title = f'Electricity Generation in {selected_entity}',
        width=150, height=150
    ).interactive().to_dict()

    return electricity_consumption_pie_chart