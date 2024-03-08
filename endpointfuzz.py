import argparse
import subprocess

# Run gobuster with specified urls wordlist and status codes to blacklist, results will be saved in a file
def run_gobuster(urls, wordlist, output_file, status_codes):
    with open(output_file, 'w') as output:
        for url in urls:
            command = f"gobuster dir -u {url} -w {wordlist} -b {status_codes}"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            output.write(f"Results for {url}:\n")
            output.write(result.stdout)
            output.write("\n\n")

# Run kiterunner with specified urls and wordlist, results will be saved in a file
def run_kiterunner(urls, wordlist, output_file):
    with open(output_file, 'w') as output:
        for url in urls:
            command = f"kr scan {url} -w {wordlist}"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            output.write(f"Results for {url}:\n")
            output.write(result.stdout)
            output.write("\n\n")

# Take the endpoint from the file provided and put them in a list
def read_endpoints_from_file(file_path):
    with open(file_path, 'r') as file:
        endpoints = [line.strip() for line in file]
    return endpoints

# make the list of urls to fuzz with the url given and the endpoint file provided
def append_endpoints(base_urls, endpoints):
    appended_urls = []
    for base_url in base_urls:
        for endpoint in endpoints:
            appended_urls.append(base_url + endpoint)
    return appended_urls

# will write the results to a file
def write_to_file(data, file_path):
    with open(file_path, 'w') as file:
        for item in data:
            file.write("%s\n" % item)

# Main function with all the process
def main():
    parser = argparse.ArgumentParser(description="Run gobuster or kiterunner with specified base URLs and endpoints")
    parser.add_argument("-u", "--base_urls", nargs='+', help="Base URLs separated by spaces")
    parser.add_argument("-e", "--endpoints_file", help="Path to the endpoints file")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to the wordlist file")
    parser.add_argument("-o", "--output_file", default="results.txt", help="Path to the output file (default: results.txt)")
    parser.add_argument("-a", "--appended_urls_file", default="appended_urls.txt", help="Path to the file to write the appended URLs (default: appended_urls.txt)")
    parser.add_argument("-t", "--tool", choices=["gobuster", "kiterunner"], default="gobuster", help="Tool to use for scanning (gobuster or kiterunner, default: gobuster)")
    parser.add_argument("-sc", "--status_codes", default="404", help="Status codes to check with Gobuster (default: 404)")
    args = parser.parse_args()

    base_urls = args.base_urls
    endpoints_file = args.endpoints_file
    wordlist = args.wordlist
    output_file = args.output_file
    appended_urls_file = args.appended_urls_file
    tool = args.tool
    status_codes = args.status_codes

## If a file with the url to fuzz is provided (appended url) it will use it instead of generating it from the base urls and endpoint

    if appended_urls_file:
        with open(appended_urls_file, 'r') as file:
            appended_urls = [line.strip() for line in file]
    else:
        endpoints = read_endpoints_from_file(endpoints_file)
        appended_urls = append_endpoints(base_urls, endpoints)
        write_to_file(appended_urls, appended_urls_file)
    
    if tool == "gobuster":
        run_gobuster(appended_urls, wordlist, output_file, status_codes)
    elif tool == "kiterunner":
        run_kiterunner(appended_urls, wordlist, output_file)

if __name__ == "__main__":
    main()
