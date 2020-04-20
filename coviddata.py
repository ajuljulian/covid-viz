import os
import numpy as np
import pandas as pd
import geopandas as gpd

from bokeh.models import GeoJSONDataSource

data_dir = os.path.join("data")

def get_states_covid_data():
    
    us_states_data_file = os.path.join(data_dir, 'covid-19-data', 'us-states.csv')
    df_covid_state_data = pd.read_csv(us_states_data_file, parse_dates=["date"], index_col='date')
    
    return df_covid_state_data

def get_states_geosource_data():
    df_covid_state_data = get_states_covid_data()
    df_state_totals = df_covid_state_data[['state', 'cases', 'deaths']].groupby('state').last()

    usa_shapefile_data_file = os.path.join(data_dir, 'cb_2018_us_state_20m', 'cb_2018_us_state_20m.shp')
    contiguous_usa_shapefile = gpd.read_file(usa_shapefile_data_file)

    states = contiguous_usa_shapefile.merge(df_state_totals, left_on='NAME', right_on='state')
    states = states.loc[~states['NAME'].isin(['Alaska', 'Hawaii'])]

    state_pop_data_file = os.path.join(data_dir, 'population', 'state_pop_2018.csv')
    state_pop = pd.read_csv(state_pop_data_file)

    # Merge shapefile with population data
    pop_states = states.merge(state_pop, left_on='NAME', right_on='NAME')
    # Drop Alaska and Hawaii
    pop_states = pop_states.loc[~pop_states['NAME'].isin(['Alaska', 'Hawaii'])]
    pop_states['covid_pct'] = pop_states['cases'] / pop_states['POPESTIMATE2018'] * 100

    # Input GeoJSON source that contains features for plotting
    geosource = GeoJSONDataSource(geojson=pop_states.to_json())

    return geosource

def get_california_county_geosource_data():
    us_county_data_file = os.path.join(data_dir, 'covid-19-data', 'us-counties.csv')
    df_us_counties_covid_data = pd.read_csv(us_county_data_file, parse_dates=["date"], index_col='date')

    # filter for California only
    df_ca_counties_covid_data = df_us_counties_covid_data.where(df_us_counties_covid_data['state'] == 'California')
    df_ca_counties_covid_data = df_ca_counties_covid_data.dropna()
    df_ca_counties_covid_data['fips'] = df_ca_counties_covid_data['fips'].astype('int64')

    # each row represents the totals for the day.  So if we group by county and take the last entry,
    # it should represent the total for that county
    df_ca_counties_covid_data = df_ca_counties_covid_data.groupby('county').last()

    # add a column representing the ratio of cases to deaths
    df_ca_counties_covid_data['pct_case_to_death'] = df_ca_counties_covid_data['deaths'] /  df_ca_counties_covid_data['cases'] * 100

    # load a dataset of per county demographic data
    county_demographic_data_file = os.path.join(data_dir, 'counties', 'co-est2019-alldata.csv')
    df_ca_counties_data = pd.read_csv(county_demographic_data_file)

    # filter for California only
    df_ca_counties_data = df_ca_counties_data.where(df_ca_counties_data['STNAME'] == 'California')
    df_ca_counties_data = df_ca_counties_data.dropna()

    # FIPS is a unique code representing each county.  We will use it to merge this dataset with others.
    df_ca_counties_data['COUNTY'] = df_ca_counties_data['COUNTY'].astype('int64')

    # load California shapefile.  Represent FIPS as integer to join this dataset with others.
    ca_counties_shapefile_data_file = os.path.join(data_dir, 'CA_Counties', 'CA_Counties_TIGER2016.shp')
    ca_counties_shapefile = gpd.read_file(ca_counties_shapefile_data_file)
    ca_counties_shapefile['COUNTYFP'] = ca_counties_shapefile['COUNTYFP'].astype('int64')

    # merge California county Covid-19 data with shape data
    counties = ca_counties_shapefile.merge(df_ca_counties_covid_data, left_on='NAME', right_on='county')

    # merge California demographic data with shape data
    counties = counties.merge(df_ca_counties_data, left_on='COUNTYFP', right_on='COUNTY')

    # Create GeoJSON source data containing features for plotting
    geosource = GeoJSONDataSource(geojson=counties.to_json())

    return geosource

