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

from scripts.tab1 import tab1
from scripts.tab2 import tab2
from scripts.tab3 import tab3


data_dir = os.path.join("data")

us_states_data_file = os.path.join(data_dir, 'covid-19-data', 'us-states.csv')
df = pd.read_csv(us_states_data_file, parse_dates=["date"], index_col='date')

# Create each of the tabs
tab1 = tab1()
tab2 = tab2()
tab3 = tab3(df, "California")

# Put all the tabs into one application
tabs = Tabs(tabs=[tab1, tab2, tab3])

# Put the tabs in the current document for display
curdoc().add_root(tabs)