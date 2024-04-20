import pandas as pd
import geopandas as gpd

# For development on local machine
raw_data = pd.read_csv("data/raw/global_data_sustainable_energy.csv")
processed_data = pd.read_csv("data/preprocessed/processed_data.csv")
world = gpd.read_file("data/preprocessed/world.shp")
gdf = gpd.read_file("data/preprocessed/preprocessed_data.shp", geometry="geometry")
consump_pie_data = pd.read_csv("data/preprocessed/consump_pie_data.csv")
elec_pie_data = pd.read_csv("data/preprocessed/elec_pie_data.csv")

# For deployment on render
# raw_data = pd.read_csv("../data/raw/global_data_sustainable_energy.csv")
# processed_data = pd.read_csv("../data/preprocessed/processed_data.csv")
# world = gpd.read_file("../data/preprocessed/world.shp")
# gdf = gpd.read_file("../data/preprocessed/preprocessed_data.shp", geometry="geometry")
# consump_pie_data = pd.read_csv("../data/preprocessed/consump_pie_data.csv")
# elec_pie_data = pd.read_csv("../data/preprocessed/elec_pie_data.csv")

# Specify coordinate reference system for geospatial data
world.crs = 'EPSG:4326'
gdf.crs = 'EPSG:4326'

# simple preprocessing of gdf
rename_dict = {
    'Renewable': 'Renewable energy share in the total final energy consumption (%)',
    'Access to': 'Access to electricity (% of population)',
    'Financial': 'Financial flows to developing countries (US $)',
    'Electricit': 'Electricity from nuclear (TWh)',
    'Electric_1': 'Electricity from renewables (TWh)',
    'Electric_2': 'Electricity from fossil fuels (TWh)',
    'gdp_per_ca': 'gdp_per_capita_y'
}
gdf = gdf.rename(columns=rename_dict)

# dropdown metrics
metrics = [
    'Renewable energy share in the total final energy consumption (%)',
    'Access to electricity (% of population)',
    'Financial flows to developing countries (US $)',
    'Electricity from nuclear (TWh)',
    'Electricity from renewables (TWh)',
    'Electricity from fossil fuels (TWh)',
]