import json
import math
import numpy as np
import pandas as pd
import geopandas as gpd
from datetime import timedelta
from bokeh.io import show, output_file, output_notebook, push_notebook
from bokeh.plotting import figure
from bokeh.models import (NumeralTickFormatter, BasicTickFormatter, CDSView, ColorBar, ColumnDataSource,
                          CustomJS, CustomJSFilter, 
                          GeoJSONDataSource, HoverTool,
                          LinearColorMapper, Slider, Panel)
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.layouts import column, row, gridplot, widgetbox
from bokeh.palettes import brewer
from bokeh.models.widgets import Select, TableColumn, DataTable, CheckboxGroup

def tab3(df, state):

    def change_state(attr, old, new):
        new_source = state_data[new]
        source.data = new_source
        
    tools = HoverTool(
        tooltips=[
            ('state', '@state'),
            ('date', '@date{%F}'),
            ('cases', '@cases'),
            ('deaths', '@deaths'),
        ],
        formatters={'@date': 'datetime'},
    )

    p = figure(x_axis_type="datetime", plot_width=900, plot_height=350, title="Covid-19 Growth",
               toolbar_location=None)

    # https://stackoverflow.com/questions/50285405/bokeh-the-widths-of-vertical-bars-doesnt-change
    # for datetime axes, the unit is milliseconds since epoch.  So something like width=0.9 will
    # only display a vertical line.  We either have to make it much larger or use timedelta the
    # way I've done below.
    #p.vbar(x='date', top='cases', width=timedelta(days=22/24), source=df_one_state.iloc[-40:])

    p.add_tools(tools)

    p.xaxis.major_label_orientation = math.pi/2
    p.xaxis.axis_label = "Date"
    p.yaxis.axis_label = "Total"
    p.yaxis.formatter = BasicTickFormatter(use_scientific=False)
    
    states = sorted(list(df['state'].unique()))
    
    state_data = {}
    for state in states:
        df_state = df.where(df['state'] == state).dropna()
        state_data[state] = df_state[-40:]
        
    source = ColumnDataSource(data=state_data[states[0]])
    
    select = Select(title="State:", value=states[0], options=states, width=300)
    select.on_change('value', change_state)
    
    p.vbar(x='date', top='cases', width=timedelta(days=22/24), source=source)

    grid = gridplot([[select], [p],], plot_width=900, plot_height=350)
 
    tab = Panel(child=grid, title='US States')
    
    return tab