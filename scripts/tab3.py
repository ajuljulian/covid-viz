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

    plot_options = dict(width=900, plot_height=350, tools='pan,lasso_select,box_select,wheel_zoom,reset')
    
    p1 = figure(x_axis_type="datetime", title="Covid-19 Growth",
               **plot_options)

    p1.add_tools(tools)
    
    states = sorted(list(df['state'].unique()))
    
    state_data = {}
    for state in states:
        df_state = df.where(df['state'] == state).dropna()
        df_state['pct_change_cases'] = df_state['cases'].pct_change() * 100
        df_state['pct_change_deaths'] = df_state['deaths'].pct_change() * 100
        state_data[state] = df_state[-40:]
        
    source = ColumnDataSource(data=state_data[states[0]])
    
    select = Select(title="State:", value=states[0], options=states, width=300)
    select.on_change('value', change_state)
    
    # https://stackoverflow.com/questions/50285405/bokeh-the-widths-of-vertical-bars-doesnt-change
    # for datetime axes, the unit is milliseconds since epoch.  So something like width=0.9 will
    # only display a vertical line.  We either have to make it much larger or use timedelta the
    # way I've done below.
    p1.vbar(x='date', top='cases', width=timedelta(days=22/24), source=source)
    
    p2 = figure(x_axis_type="datetime", x_range=p1.x_range, title="Covid-19 Cases % Growth",
           **plot_options)
    p2.line(x='date', y='pct_change_cases', source=source)
    p2.add_tools(tools)
    
    p3 = figure(x_axis_type="datetime", x_range=p1.x_range, title="Covid-19 Deaths % Growth",
           **plot_options)
    p3.line(x='date', y='pct_change_deaths', source=source)
    p3.add_tools(tools)
    
    p1.xaxis.major_label_orientation = math.pi/3
    p1.xaxis.axis_label = "Date"
    p1.yaxis.axis_label = "Total"
    p1.yaxis.formatter = BasicTickFormatter(use_scientific=False)
    
    p2.xaxis.formatter.days = '%m/%d'
    p2.xaxis.major_label_orientation = math.pi/3
    p2.xaxis.axis_label = "Date"
    p2.yaxis.axis_label = "Total"
    
    p3.xaxis.formatter.days = '%m/%d'
    p3.xaxis.major_label_orientation = math.pi/3
    p3.xaxis.axis_label = "Date"
    p3.yaxis.axis_label = "Total"

    grid = gridplot([[select], [p1], [p2], [p3]])
 
    tab = Panel(child=grid, title='US States')
    
    return tab