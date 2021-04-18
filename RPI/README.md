## Screenshots

### Overview

![overview](screenshots/overview.png)

### Details

![details](screenshots/details.png)

## Waste Classifier

### Materials needed

3x LEDs
1x Button
4x Resistors
1x Breadboard

Setup above equipment according to pin layout in `rpi_waste_classifier.py`

Download model from https://nusu-my.sharepoint.com/:u:/r/personal/e0311162_u_nus_edu/Documents/classification%20model/trash-dataset-v3%20TFLite.zip?csf=1&web=1

Unzip and rename folder to `model` and place in the same directory as `rpi_waste_classifier.py`

Requirements

```
pip3 install https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp37-cp37m-linux_armv7l.whl

pip3 install lobe
```

Run program with python3

Current drawbacks

- Label for `no item` added, works sometimes

### Dataset used

https://github.com/garythung/trashnet

`dataset-resized.zip`

The categories cardboard, glass, metal, paper, plastic was placed under `recyclable` label, while trash was placed under `general trash` label.

There is a much greater set of images that for the `recyclable` label, so by default the model might predict `recyclable` when shown something random.

## Structure

Repo to store all functionality related to web platform, including flask server, and serial communication between microbit and RPi

### flask_app

`views.py`

Plan is to use this for template views

`api.py`

Plan is to use this for api endpoints, all routes prefixed with '/api'

See example SQL queries here

**Misc**

Bootstrap CSS library added with some custom overrides. Compiled from scss source files.

**examples**

`localhost:5000/` mockup for bin fill level

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
mkdir instance
python3 -m flask init-db

python3 -m flask run
```
