#!/bin/bash

# Check if the input file is provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 <input_file> <output_file>"
    exit 1
fi

input_file=$1
output_file=$2

# Check if the input file exists
if [ ! -f "$input_file" ]; then
    echo "Input file not found: $input_file"
    exit 1
fi

# Loop through each server in the input file
while IFS= read -r server; do
    echo "Checking server: $server"
    # Run nslookup and capture the output
    result=$(nslookup "$server")
    
    # Check if the server is up by looking for an IP address in the output
    if [[ "$result" == *"Name:"* && "$result" == *"Address:"* ]]; then
        ip_address=$(echo "$result" | awk '/^Address: / { print $2 }')
        echo "Server is up. IP address: $ip_address"
        echo "$ip_address" >> "$output_file"
    else
        echo "Server is down or not found."
    fi
done < "$input_file"
