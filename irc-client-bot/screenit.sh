#!/bin/bash

dest=/media/dns-345-0/Volume_1/share/irssi

screen -dmS get_file_$(date +%s) -- python3 GetFile.py --filename "$1"

screen -dmS xferit_$(date +%s) -- ./xferit.sh "$1"
