#!/bin/bash

# Activate the conda environment
conda activate real_estate

# Receive the input for overwrite
read -p "Overwrite the JSON file? (Y/N): " overwrite

# Get the current date
actual_date=$(date +"%Y-%m-%d")

# save_directory="saved_json/$actual_date"

if [ "$overwrite" == "Y" ]; then
    # Run scrapy crawl with overwrite option
    scrapy crawl viva -O "crawler/saved_json/$actual_date.json"
elif [ "$overwrite" == "N" ]; then
    # Confirm if the JSON file should be overwritten
    read -p "Are you sure you want to overwrite the JSON file? (Y/N): " confirm_overwrite
    if [ "$confirm_overwrite" == "Y" ]; then
        scrapy crawl viva -o "crawler/saved_json/$actual_date.json"
    else
        echo "JSON file will not be overwritten."
    fi
else
    echo "Incorrect overwrite input. Please provide 'Y' or 'N'."
fi
