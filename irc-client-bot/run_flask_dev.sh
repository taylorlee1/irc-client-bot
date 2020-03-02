#!/bin/bash

source bin/activate
FLASK_ENV=development FLASK_APP=xdcc_api.py python3 -m flask run --host=0.0.0.0
