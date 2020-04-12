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
from bokeh.models.widgets import Tabs

from scripts.map import map_tab
from scripts.heatmap import heatmap_tab
from scripts.clusters import clusters_tab
from scripts.clusters_by_metrics import clusters__by_metrics_tab


data_dir = os.path.join('international_growth_app', "data")

shapefile = os.path.join(data_dir, 'ne_110m_admin_0_countries', 'ne_110m_admin_0_countries.shp')

gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]

gdf.columns = ['country', 'country_code', 'geometry']

# Drop Antarctica
gdf = gdf.drop(gdf.index[159])

stats_file_path = os.path.join(data_dir, 'top_50_markets.xlsx')
df = pd.read_excel(stats_file_path, sheet_name=0)

kpi_columns = list(set(df.columns) - set(['country_code', 'Country']))

# Replace spaces with underscores.  Bokeh has difficulty dealing with spaces in column names
renamed_columns = {w: "_".join(re.findall(r'\w+', w)) for w in kpi_columns}

df = df[['country_code', 'Country'] + kpi_columns].copy()

kpi_columns = list(renamed_columns.values())
kpi_columns.sort()

df = df.rename(columns=renamed_columns)

df_countries = pd.read_csv(os.path.join(data_dir, 'countries_gapminder.csv'))

df.dropna(inplace=True)
print(df.head())

# Metrics
df_kpi = pd.read_excel(stats_file_path, sheet_name=1)
df_kpi = df_kpi.set_index(list(df_kpi.columns)[0])

# Create each of the tabs
tab_map = map_tab(df, gdf, kpi_columns)
tab_heatmap = heatmap_tab(df, kpi_columns)
tab_clusters = clusters_tab(df, kpi_columns)
tab_clusters_by_metrics = clusters__by_metrics_tab(df, kpi_columns, df_kpi)

# Put all the tabs into one application
tabs = Tabs(tabs = [tab_map, tab_heatmap, tab_clusters, tab_clusters_by_metrics])

# Put the tabs in the current document for display
curdoc().add_root(tabs)