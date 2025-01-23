#!/bin/bash

# List of directories to create
directories=("jarjestelemattomat" "puut" "numerot" "elaimet" "pizzataytteet" "muut")

# Loop and create
for directory in "${directories[@]}"; do
    mkdir -p "$directory"
done

# List of empty files to create
items=("kissa" "koivu" "kuusi" ".nakymatonlaama" "kinkku" "ananas" "avaruus" "diskurssi")

# Add empty files to jarjestelemattomat
for item in "${items[@]}"; do
    touch "jarjestelemattomat/$item"
done
