#!/bin/bash

screen -dmS get_file_$(date +%s) -- python3 GetFile.py --filename "$1"
