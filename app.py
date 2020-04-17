import numpy as np
import pandas as pd
import math
import yaml
import json
import re
import random
import os
import geopandas as gpd

from bokeh.io import curdoc
from bokeh.models import GeoJSONDataSource
from bokeh.models.widgets import Tabs

from scripts.tab1 import tab1
from scripts.tab2 import tab2
from scripts.tab3 import tab3


data_dir = os.path.join("data")

us_states_data_file = os.path.join(data_dir, 'covid-19-data', 'us-states.csv')
df = pd.read_csv(us_states_data_file, parse_dates=["date"], index_col='date')

df_state_totals = df[['state', 'cases', 'deaths']].groupby('state').last()

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

# Create each of the tabs
tab1 = tab1()
tab2 = tab2(geosource)
tab3 = tab3(df)

# Put all the tabs into one application
tabs = Tabs(tabs=[tab1, tab2, tab3])

# Put the tabs in the current document for display
curdoc().add_root(tabs)