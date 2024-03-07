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

## endpointfuzz.py

This script will append urls with a list of endpoints. Say you have found multiple possible api endpoints and want to fuzz them on multiple urls. This willdo this for you.

 1. The enddpoints will be created with the urls and the list of endpoints you will provide
 2. Each new endpoint created will be fuzzed using gobuster.
 3. Gobuster results will be in an output file.


### How to use

- `python3 endpointfuzz.py -u http://example.com -e endpoints.txt -w wordlist.txt -o outputfile`
- You might need to adapt the gobuster command to your context and choose which error message to hide.
