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

def tab1(geosource):

    # Define color palettes
    palette = brewer['Reds'][8]
    palette = palette[::-1] # reverse order of colors so higher values have darker colors

    # Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
    color_mapper = LinearColorMapper(palette=palette, low=0, high=10)

    # Create color bar.
    color_bar = ColorBar(color_mapper=color_mapper, 
                     label_standoff=8,
                     width=500, height=20,
                     border_line_color=None,
                     location=(0,0), 
                     orientation='horizontal',
                    )

    # Create figure object.
    p = figure(title='Covid-19 cases', 
           plot_height = 950, plot_width = 900, 
           toolbar_location = 'below',
           tools='pan, wheel_zoom, box_zoom, reset')

    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

    # Add patch renderer to figure.
    counties = p.patches('xs', 'ys', source=geosource,
                   fill_color = {'field' :'pct_deaths_to_cases',
                                 'transform' : color_mapper},
                   line_color = 'black', 
                   line_width = 0.25, 
                   fill_alpha = 1)
    # Create hover tool
    p.add_tools(HoverTool(renderers = [counties],
                      tooltips = [('County','@NAME'),
                                  ('Cases', '@cases'),
                                  ('Deaths', '@deaths'),
                                  ('Deaths to Cases', '@pct_deaths_to_cases%')
                                 ]))
    # Specify layout
    p.add_layout(color_bar, 'below')
    
    tab = Panel(child=p, title='California Counties')
    
    return tab