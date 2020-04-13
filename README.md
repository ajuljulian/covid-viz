# Installation Steps

1. CD to top-most directory

1. Create a new anaconda environment

    `$ conda create -n covid-viz python=3`

1. Activate environment

    `$ conda activate covid-viz`

1. Install required packages

    `$ conda install --yes --file requirements.txt`

1. Launch Bokeh app

    `$ bokeh serve --show main.py`

