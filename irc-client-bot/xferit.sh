#!/bin/bash

set -x

now=$(date +%s)
maxtime=$((now+3600*24*5))

dest=/media/dns-345-0/Volume_1/share/irssi

while [[ 1 ]]; do
  files=$(find "$1" -mmin +5)
  if [[ "$files" == "$1" ]]; then
    break
  fi
  sleep $((60*5))
  if [[ $(date +%s) -gt $maxtime ]]; then
    exit 222
  fi
done
rsync --remove-source-files $1 $dest/$1

ln -sf $dest/$1 $1
