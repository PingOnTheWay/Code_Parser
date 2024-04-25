import os

# Directory containing the log files
log_dir = '/Users/pingwan/Desktop/Thesis_Project/Code_Parser/data'

# Output file to save the first lines
output_file = '/Users/pingwan/Desktop/Thesis_Project/Code_Parser/output/first_lines.log'

# Get a list of all files in the directory 
log_files = [f for f in os.listdir(log_dir) if f.endswith('.txt')]

# Open the output file for writing
with open(output_file, 'w') as outfile:
    # Iterate over each log file
    for log_file in log_files:
        # Construct the full path to the log file
        log_file_path = os.path.join(log_dir, log_file)
        # Open the log file for reading
        with open(log_file_path, 'r') as infile:
            # Read the first line
            infile.readline()
            infile.readline()
            first_line = infile.readline()
            # Write the first line to the output file
            outfile.write(first_line)

print(f"First lines from all log files have been saved to {output_file}.")