#!/bin/bash

DIR="News_$(date +"%d_%m_%Y")"

if [ -d "data/$DIR" ]; then

    exit 1

else 

    mkdir "data/$DIR"
    exit 0

fi