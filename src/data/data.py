import pandas as pd
import geopandas as gpd

# For development on local machine
world = gpd.read_parquet("data/preprocessed/world_countries.parquet")
gdf = gpd.read_parquet("data/preprocessed/preprocessed_gdf.parquet")
consump_pie_data = pd.read_parquet("data/preprocessed/consump_pie_data.parquet")
elec_pie_data = pd.read_parquet("data/preprocessed/elec_pie_data.parquet")
access_to_electricity = pd.read_parquet("data/preprocessed/access_to_electricity.parquet")
financial_flow = pd.read_parquet("data/preprocessed/financial_flow.parquet") 
gdp_per_capita = pd.read_parquet("data/preprocessed/gdp_per_capita.parquet")
population = pd.read_parquet("data/preprocessed/population_df.parquet")

# For deployment on render
# world = gpd.read_parquet("../data/preprocessed/world_countries.parquet")
# gdf = gpd.read_parquet("../data/preprocessed/preprocessed_gdf.parquet")
# consump_pie_data = pd.read_parquet("../data/preprocessed/consump_pie_data.parquet")
# elec_pie_data = pd.read_parquet("../data/preprocessed/elec_pie_data.parquet")
# access_to_electricity = pd.read_parquet("../data/preprocessed/access_to_electricity.parquet")
# financial_flow = pd.read_parquet("../data/preprocessed/financial_flow.parquet") 
# gdp_per_capita = pd.read_parquet("../data/preprocessed/gdp_per_capita.parquet")
# population = pd.read_parquet("../data/preprocessed/population_df.parquet")

# Specify coordinate reference system for geospatial data
world.crs = 'EPSG:4326'
gdf.crs = 'EPSG:4326'

# dropdown metrics
metrics = [
    'Renewable energy share in the total final energy consumption (%)',
    'Access to electricity (% of population)',
    'Financial flows to developing countries (US $)',
    'Electricity from nuclear (TWh)',
    'Electricity from renewables (TWh)',
    'Electricity from fossil fuels (TWh)',
]