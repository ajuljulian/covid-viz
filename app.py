import os

from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

from scripts.tab1 import tab1
from scripts.tab2 import tab2
from scripts.tab3 import tab3

import coviddata

data_dir = os.path.join("data")

df_covid_states_data = coviddata.get_states_covid_data()

geosource_states_data = coviddata.get_states_geosource_data()

# Create each of the tabs
tab1 = tab1(coviddata.get_california_county_geosource_data())
tab2 = tab2(geosource_states_data)
tab3 = tab3(df_covid_states_data)

# Put all the tabs into one application
tabs = Tabs(tabs=[tab1, tab2, tab3])

# Put the tabs in the current document for display
curdoc().add_root(tabs)