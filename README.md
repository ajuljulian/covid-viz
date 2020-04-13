# Installation Steps

1. CD to top-most directory

1. Create a new anaconda environment

    `$ conda create -n covid-viz python=3`

1. Activate environment

    `$ conda activate covid-viz`

1. Install required packages

    `$ conda install --yes --file requirements.txt`

# Running Locally

1. Start the bokeh server

    `$ bokeh serve --show app.py`

# Deploying to Heroku

1. Install Heroku cli tools

    `$ brew tap heroku/brew && brew install heroku`

1. Login to Heroku

    `$ heroku login -i`

1. CD to top-most directory

1. Create Heroku app

    `$ heroku create`

1. Make sure that a git remote named heroku has been set up

    `$ git remote -v`

    You should see fetch and push remotes are set up, something like this:

    `heroku  https://git.heroku.com/thawing-inlet-61413.git (fetch)`
    `heroku  https://git.heroku.com/thawing-inlet-61413.git (push)`

1. Update Procfile with name of the heroku app

1. Push to heroku

    `git push heroku master`

1. Go to the heroku url you got in the last step

