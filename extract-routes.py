import os
import re

# Base directory where your Java source code is located -> Replace with the actual path in your context
BASE_DIR = 'path/to/src/main/java'

# Patterns to search for
patterns = [
    r'getRequestURI\(\)',          # To find where URLs are being extracted
    r'getPathInfo\(\)',            # To find path info
    r'sendRedirect\(["\'](.*?)["\']',  # To find redirect URLs
    r'forward\(["\'](.*?)["\']',       # To find forward URLs
    r'@WebServlet\(["\'](.*?)["\']',   # To find annotated servlets if any
    r'url-pattern>(.*?)</url-pattern>',  # For URL patterns in web.xml
    r'"(/[^"]*?)"'                 # General pattern to catch URLs in string literals
]

# Dictionary to store found URLs
found_urls = {}

# Function to search for patterns in a file
def search_patterns_in_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        for pattern in patterns:
            matches = re.findall(pattern, content)
            if matches:
                found_urls[file_path] = found_urls.get(file_path, []) + matches

# Recursively search all Java files in the directory
for root, _, files in os.walk(BASE_DIR):
    for file in files:
        if file.endswith('.java'):
            search_patterns_in_file(os.path.join(root, file))

# Display the found URLs
for file, urls in found_urls.items():
    print(f"File: {file}")
    for url in urls:
        print(f"  URL/Pattern: {url}")
