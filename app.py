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


data_dir = os.path.join('covid-19', "data")

# Create each of the tabs
tab1 = tab1()
tab2 = tab2()

# Put all the tabs into one application
tabs = Tabs(tabs=[tab1, tab2])

# Put the tabs in the current document for display
curdoc().add_root(tabs)