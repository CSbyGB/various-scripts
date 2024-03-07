def merge_files(file_paths, output_file):
    merged_content = set()

    # Read contents of each file and merge into a single set to avoid duplicates
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            for line in file:
                merged_content.add(line.strip())

    # Write the merged content into the output file
    with open(output_file, 'w') as output:
        for line in merged_content:
            output.write(line + '\n')

# Will probably add a main function at some point
# Process with the merging
file_paths = ['wordlist1.txt', 'wordlist2.txt', 'wordlist3.txt']
output_file = 'merged_wordlist.txt'

merge_files(file_paths, output_file)
