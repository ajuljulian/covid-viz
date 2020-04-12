import math
import numpy as np
from bokeh.plotting import figure
from bokeh.models import Panel

def tab2():

    p = figure(plot_width=700, plot_height=600)

    x = np.linspace(-math.pi/2, math.pi/2)
    y = np.cos(x)

    p.line(x, y)
    
    tab = Panel(child=p, title='Tab 2')
    
    return tab