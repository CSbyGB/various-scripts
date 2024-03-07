# various-scripts
this repo will host various scripts

## isitup.sh

This script takes a list of server from a txt file and run nslookup on each of them.
It returns true if the server is up and display its ip address. It will also generate a list of the ip address of the servers that are up.

### How to use

- `./check_servers.sh server_list.txt up_servers.txt`

## mergeWordlists.py

This script will merge multiple wordlist into one file without duplicates

### How to use

Add in the `file_paths` variable this list of files you want to merge together.
