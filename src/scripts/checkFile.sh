#!/bin/bash

FILEPATH="$1"
DATE=$(date +"%d_%m_%Y")

if [ -e "$FILEPATH" ]; then
    # File exist
    exit 0
else
    exit 1
fi