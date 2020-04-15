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

    def get_data_for_state(state):
        df_one_state = df.where(df['state'] == state)
        df_one_state = df_one_state.dropna()
        df_one_state['pct_change_cases'] = df_one_state['cases'].pct_change() * 100
        df_one_state['pct_change_deaths'] = df_one_state['deaths'].pct_change() * 100

        return df_one_state

    def change_state(attr, old, new):
        pass
    
    tools = HoverTool(
        tooltips=[
            ('date', '@date{%F}'),
            ('cases', '@cases'),
            ('cases % change', '@pct_change_cases{0.00}%'),
            ('deaths', '@deaths'),
            ('deaths % change', '@pct_change_deaths{0.00}%')
        ],
        formatters={'@date': 'datetime'},
    )

    states = sorted(list(df['state'].unique()))

    source = ColumnDataSource(data=dict(
        state=states,
        data=[get_data_for_state(state) for state in states]
    ))

    df_one_state = get_data_for_state(state)

    p1 = figure(x_axis_type="datetime", title="Covid-19 Total Cases in {}".format(state),
               toolbar_location=None)
    
    select = Select(title="State:", value=states[0], options=states, width=300)

    # https://stackoverflow.com/questions/50285405/bokeh-the-widths-of-vertical-bars-doesnt-change
    # for datetime axes, the unit is milliseconds since epoch.  So something like width=0.9 will
    # only display a vertical line.  We either have to make it much larger or use timedelta the
    # way I've done below.
    p1.vbar(x='date', top='cases', width=timedelta(days=22/24), source=df_one_state.iloc[-40:])
    p1.add_tools(tools)

    p2 = figure(x_axis_type="datetime", x_range=p1.x_range, title="Covid-19 Cases % Growth in {}".format(state),
               toolbar_location=None)
    p2.line(x='date', y='pct_change_cases', source=df_one_state.iloc[-40:])
    p2.add_tools(tools)

    p3 = figure(x_axis_type="datetime", x_range=p1.x_range, title="Covid-19 Deaths % Growth in {}".format(state),
               toolbar_location=None)
    p3.line(x='date', y='pct_change_deaths', source=df_one_state.iloc[-40:])
    p3.add_tools(tools)

    p1.xaxis.formatter.days = '%m/%d/%Y'
    p1.xaxis.major_label_orientation = math.pi/3
    p1.xaxis.axis_label = "Date"
    p1.yaxis.axis_label = "Total"

    p2.xaxis.formatter.days = '%m/%d/%Y'
    p2.xaxis.major_label_orientation = math.pi/3
    p2.xaxis.axis_label = "Date"
    p2.yaxis.axis_label = "Total"

    p3.xaxis.formatter.days = '%m/%d/%Y'
    p3.xaxis.major_label_orientation = math.pi/3
    p3.xaxis.axis_label = "Date"
    p3.yaxis.axis_label = "Total"

    grid = gridplot([[select], [p1],[p2],[p3]], plot_width=900, plot_height=350)
 
    tab = Panel(child=grid, title='Tab 3')
    
    return tab