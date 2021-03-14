## Structure

Repo to store all functionality related to web platform, including flask server, and serial communication between microbit and RPi


### flask_app

`views.py`

Plan is to use this for template views

`api.py`

Plan is to use this for api endpoints, all routes prefixed with '/api'

**Misc**

Bootstrap CSS library added with some custom overrides. Compiled from scss source files.

**examples**

`localhost:5000/` mockup for bin fill level

`localhost:5000/bin/all` returns mock data from db


## Setup

Install Python 3

Setup virtualenv

```
pip3 install virtualenv
python3 -m virtualenv venv
source venv/bin/activate
```

Install required packages
```
pip3 install -r requirements.txt
```

**Run flask app**
```
# windows
set FLASK_ENV=development
set FLASK_APP=flask_app
OR
# unix
export FLASK_ENV=development
export FLASK_APP=flask_app

# initialise db
# create instance folder to store sqlite db
touch instance
python3 -m flask init-db

python3 -m flask run
```
