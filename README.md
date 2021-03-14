## Structure

Repo to store all functionality related to web platform, including flask server, and serial communication between microbit and RPi


### flask_app

`app.py`

Main entry point. Plan is to use this for template views

`api.py`

Plan is to use this for api endpoints, all routes prefixed with '/api'

**Misc**

Bootstrap CSS library added with some custom overrides. Compiled from scss source files.


## Setup

Install Python 3

Setup virtualenv if desired

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
OR
# unix
export FLASK_ENV=development

cd flask_app
python3 -m flask run
```
