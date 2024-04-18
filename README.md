# various-scripts

> This repo will host various scripts

## isitup.sh

This script takes a list of server from a txt file and run nslookup on each of them.
It returns true if the server is up and display its ip address. It will also generate a list of the ip address of the servers that are up.

### How to use

- `./check_servers.sh server_list.txt up_servers.txt`
## reduce-img.sh

This script will reduce the images of your current folder if they are bigger than 1 Mo.  

### Requires

You need to install `ImageMagick` you can do so with `sudo apt install imagemagick`

### How to use

- Go in the folder with the images you want to resize and run it `./reduce-img.sh`

## mergeWordlists.py

This script will merge multiple wordlists into one file without duplicates

### How to use

Add in the `file_paths` variable this list of files you want to merge together.

## endpointfuzz.py

This script is a tool for running either Gobuster or Kiterunner to perform directory/file brute-forcing attacks on web servers. It allows users to specify base URLs and endpoints (or a file containing a list of URLs) along with a wordlist to use for the attack. The results of the scan are saved to an output file.

### How to use

1. Required Arguments:

    -w, --wordlist: Path to the wordlist file containing directory and file paths to brute force.

2. Optional Arguments:

    -u, --base_urls: Base URLs separated by spaces.  
    -e, --endpoints_file: Path to the file containing endpoint paths to append to base URLs.  
    -o, --output_file: Path to the output file where scan results will be saved (default: results.txt).  
    -a, --appended_urls_file: Path to the file containing appended URLs (default: appended_urls.txt).  
    -t, --tool: Choose between "gobuster" or "kiterunner" (default: gobuster).  
    -sc, --status_codes: Status codes to check with Gobuster (default: 404).  

3. How to Run:

- To perform a scan using base URLs and endpoint files:

```bash
python3 script.py -u <base_url1> <base_url2> -e <endpoints_file> -w <wordlist_file>
```

- To perform a scan using appended URLs file:

```bash
python3 script.py -a <appended_urls_file> -w <wordlist_file>
```
Additionally, you can specify the tool (gobuster or kiterunner) using the `-t` flag.

### Requirements

- Python: you must have python installed
- Gobuster or Kiterunner: Depending on the chosen tool (-t or --tool argument), the respective tool (gobuster or kiterunner) must be installed and available in the system's PATH.
- Wordlist File: you will need a good wordlist to provide. Kiterunner provide wordlists on their official repo [here](https://github.com/assetnote/kiterunner) and for gobuster you can use [SecLists](https://github.com/danielmiessler/SecLists), or the ones provided with your OS or your the ones you prefer.
