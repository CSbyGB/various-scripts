import argparse
import subprocess

def run_gobuster(urls, wordlist, output_file):
    with open(output_file, 'w') as output:
        for url in urls:
            command = f"gobuster dir -u {url} -w {wordlist} -b 302,404,403"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            output.write(f"Results for {url}:\n")
            output.write(result.stdout)
            output.write("\n\n")

def read_endpoints_from_file(file_path):
    with open(file_path, 'r') as file:
        endpoints = [line.strip() for line in file]
    return endpoints

def append_endpoints(base_urls, endpoints):
    appended_urls = []
    for base_url in base_urls:
        for endpoint in endpoints:
            appended_urls.append(base_url + endpoint)
    return appended_urls

def main():
    parser = argparse.ArgumentParser(description="Run gobuster with specified base URLs and endpoints")
    parser.add_argument("-u", "--base_urls", nargs='+', help="Base URLs separated by spaces")
    parser.add_argument("-e", "--endpoints_file", help="Path to the endpoints file")
    parser.add_argument("-w", "--wordlist", help="Path to the wordlist file")
    parser.add_argument("-o", "--output_file", default="gobuster_results.txt", help="Path to the output file (default: gobuster_results.txt)")
    args = parser.parse_args()

    base_urls = args.base_urls
    endpoints_file = args.endpoints_file
    wordlist = args.wordlist
    output_file = args.output_file

    endpoints = read_endpoints_from_file(endpoints_file)
    appended_urls = append_endpoints(base_urls, endpoints)

    run_gobuster(appended_urls, wordlist, output_file)

if __name__ == "__main__":
    main()
