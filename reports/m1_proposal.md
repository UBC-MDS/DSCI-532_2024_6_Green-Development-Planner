# Motivation and Purpose
Role: Renewable Energy Development Advisory

Target Audience: Policymakers and Funding Organizations

Our initiative is centered on the pivotal goal of enhancing renewable energy infrastructures in developing countries, where the need for sustainable and accessible energy solutions is most critical. With limited resources for such significant aid funds, the challenge lies in identifying and prioritizing funding opportunities that promise the highest impact on sustainable development and energy access.

Our proposed data visualization dashboard is designed to streamline this decision-making process. It will enable policymakers and funding organizations to identify and prioritize aid funds in renewable energy with the highest potential for impact. By aggregating and visualizing key data on energy access, current energy mix, and renewable potential, the dashboard provides a clear, data-driven basis for directing funds.

This tool aims to ensure efficient and equitable use of resources, supporting a transition to sustainable energy in underserved regions. This focused approach aims to facilitate informed decisions, helping to accelerate global efforts towards a cleaner, more sustainable energy future.

# Description and Data

The dataset used in this project provides comprehensive insights into sustainable energy indicators and related factors across different countries from the year of 2000 to 2020. It enables analysis of crucial aspects such as electricity access, renewable energy adoption, carbon emissions, financial flows, and economic growth. Researchers can compare nations, monitor progress towards sustainable development goals, and gain deep insights into global energy consumption trends over time.

The dataset consists a total of 21 variables. Here is summary table:

| Variable Name                                            | Datatype (default)          | Description                                                                                     |
|----------------------------------------------------------|-----------------------------|-------------------------------------------------------------------------------------------------|
| Entity                                                   | Object                      | The name of the country or region for which the data is reported.                              |
| Year                                                     | Integer                     | The year for which the data is reported, spanning from 2000 to 2020.                            |
| Access to electricity (% of population)                 | Float                       | The percentage of the population with access to electricity.                                    |
| Access to clean fuels for cooking (% of population)     | Float                       | The percentage of the population primarily relying on clean fuels for cooking.                   |
| Renewable-electricity-generating-capacity-per-capita    | Float                       | The generating capacity of renewable electricity per capita (watts per capita)                   |
| Financial flows to developing countries (US $)         | Float                       | The dollar amount in aid and assistance from developed countries for clean energy projects.      |
| Renewable energy share in total final energy consumption (%) | Float                   | The percentage of renewable energy in final energy consumption.                                  |
| Electricity from fossil fuels (TWh)                    | Float                       | The amount of electricity generated from fossil fuels (coal, oil, gas) in terawatt-hours.        |
| Electricity from nuclear (TWh)                          | Float                       | The amount of electricity generated from nuclear power in terawatt-hours.                        |
| Electricity from renewables (TWh)                       | Float                       | The amount of electricity generated from renewable sources (hydro, solar, wind, etc.) in TWh.    |
| Low-carbon electricity (% electricity)                  | Float                       | The percentage of electricity from low-carbon sources (nuclear and renewables).                   |
| Primary energy consumption per capita (kWh/person)      | Float                       | The amount of primary energy consumption per capita in kilowatt-hours.                           |
| Energy intensity level of primary energy (MJ/$2011 PPP GDP) | Float                   | The amount of energy supplied to the economy per unit value of economic output.                  |
| CO2 emissions (metric tons per capita)                  | Float                       | The amount of carbon dioxide emissions per capita in metric tons.                                |
| Renewables (% equivalent primary energy)                | Float                       | The percentage of equivalent primary energy derived from renewable sources.                       |
| GDP growth (annual %)                                   | Float                       | The annual GDP growth rate based on constant local currency.                                     |
| GDP per capita                                          | Float                       | The gross domestic product per capita of the country.                                            |
| Population Density (P/Km2)                              | Object                      | The population density in persons per square kilometer.                                           |
| Land Area (Km2)                                         | Float                       | The total land area in square kilometers.                                                       |
| Latitude                                                 | Float                       | The latitude of the country's centroid in decimal degrees.                                       |
| Longitude                                                | Float                       | The longitude of the country's centroid in decimal degrees.                                      |

Based on our research question, our primary focus will be on several key variables, namely: `Entity`, `Year`, `Electricity from fossil fuels (TWh)`, `Electricity from nuclear (TWh)`, `Electricity from renewables (TWh)`, `Financial flows to developing countries (US $)`, `Renewable energy share in total final energy consumption (%)`, and `Access to electricity (% of population)`. By analyzing these variables, we aim to construct visualizations that facilitate the identification of countries with significant potential for green development.

# Research Question  

Mary is a policy advisor focusing on enhancing energy access and promoting renewable energy initiatives globally. Mary's role involves identifying countries / regions where the funding and resources can significantly boost their transition towards sustainable energy, particularly in areas lagging behind in electricity access and clean energy.  

Mary aims to prioritize funding to countries that are most in need of clean energy infrastructure. She also aims for a decision-making process that is evidence-based and transparent, in order to foster trust and clarity among stakeholders.  

When Mary accesses the dashboard, she can view a world map where each country is shaded in a color that corresponds to its specific value for a chosen variable, such as 'Electricity from fossil fuels'. Additionally, the dashboard offers interactive tools that enable Mary to delve into the detailed statistics of a particular country, examining aspects such as the country's access to electricity, gaps between fossil fuel and renewable energy use (hereafter 'energy gaps'), overall scale of energy production and consumption, and financial aid received.   

Specifically, Mary's task involves a few steps. First, she will look for countries with a low level of electricity access, as these countries have the greatest need for energy. Then, she will examine their energy gaps, overall scale of energy usage, and the financial aid they received. This process allows Mary to identify countries / regions that, despite significant energy gaps and limited access to electricity, have not received enough renewable energy funds.    

The dashboard enables Mary to make an informed decision. It will facilitate a funding allocation strategy that prioritizes countries with the greatest need and potential for energy usage change. Our dashboard ensures that the funding project effectively reduces global reliance on fossil fuels, boost clean energy, and promotes sustainable development in unfunded countries / regions.   

# App Sketch and Description