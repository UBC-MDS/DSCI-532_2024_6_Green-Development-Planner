from dash import callback, Output, Input
import altair as alt
import pandas as pd

from data.data import consump_pie_data, elec_pie_data

# Callback to update the energy consumption pie chart based on selected country
@callback(
    Output('pie-chart', 'spec'),
    Input('entity-dropdown', 'value')
)
def update_energy_consumption_chart(selected_entity):

    pie_data = consump_pie_data[consump_pie_data['Entity'] == selected_entity]
    
    # Specify legend titles and colors
    domain = ['Renewables', "Other"]
    range_ = ['#4CBB17', '#DDDDDD']

    # Plot pie chart
    # energy_consumption_pie_chart = alt.Chart(pie_data).mark_arc(innerRadius=50).encode(
    #     theta='value',
    #     color=alt.Color('category', legend=alt.Legend(title='Energy Source')).scale(domain=domain, range=range_),
    #     tooltip=['category', 'value']
    # ).properties(
    #     title={"text": ["Energy Consumption", f"in {selected_entity}"]},
    #     width='container', height=150
    # ).interactive().to_dict()
    
    # Base pie chart
    base1 = alt.Chart(pie_data).encode(
    theta=alt.Theta('value:Q', stack=True),  # Ensure values are quantitative and stacked
    color=alt.Color('category:N', legend=alt.Legend(title='Energy Source'), scale=alt.Scale(domain=domain, range=range_)),  # Named categories
    tooltip=['category', 'value']
    )
    # Add arc for pie chart
    pie1 = base1.mark_arc(innerRadius=40)

    text1 = base1.mark_text(radius=90, size=15, align="center").encode(
        text='Percentage:N'
    )

    energy_consumption_pie_chart = (pie1 + text1).properties(
        title={"text": ["Energy Consumption", f"in {selected_entity}"]},
        width='container', height=150
    ).interactive().to_dict()

    return energy_consumption_pie_chart

#callback to update electricity generation pie chart based on selected country
@callback(
    Output('electricity-production', 'spec'),
    Input('entity-dropdown', 'value')
)
def update_electricty_generation_chart(selected_entity):

    source = elec_pie_data[elec_pie_data['Entity'] == selected_entity]

    # Specify legend titles and colors
    domain = ['Renewables', "Fossil Fuels", "Nuclear"]
    range_ = ['#4CBB17', '#C19A6B', '#4682B4']

    # # Plot pie chart
    # electricity_consumption_pie_chart = alt.Chart(source).mark_arc(innerRadius=50).encode(
    #     theta = 'Value',
    #     color = alt.Color('Energy Source', legend=alt.Legend(title='Energy Source')).scale(domain=domain, range=range_),
    #     tooltip=['Energy Source', 'Value']
    # ).properties(
    #     title = {"text": ["Electricity Generation", f"in {selected_entity}"]},
    #     width='container', height=150
    # ).interactive().to_dict()

    # Base pie chart
    base2 = alt.Chart(source).encode(
        theta = 'Value',
        color = alt.Color('Energy Source', legend=alt.Legend(title='Energy Source')).scale(domain=domain, range=range_),
        tooltip=['Energy Source', 'Value']
        )
    # Add arc for pie chart
    pie2 = base2.mark_arc(innerRadius=40)

    text2 = base2.mark_text(radius=90, 
                            size=15, 
                            align="center").encode(
        text=alt.Text("Percentage:Q",format=".0%",)
    )

    electricity_consumption_pie_chart = (pie2 + text2).properties(
        title={"text": ["Electricity Generation", f"in {selected_entity}"]},
        width='container', height=150
    ).interactive().to_dict()

    return electricity_consumption_pie_chart