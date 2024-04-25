import os
import json
import csv

def parse_slurm_log(file_path):
    # read just one log file and parse it as a dictionary
    with open(file_path, 'r') as file:
        data = file.read().strip().split('\n')[-1]  # read last line
        job_id, start, end, elapsed = data.split()
        return {
            "job_id": job_id,
            "start_time": start,
            "end_time": end,
            "elapsed_time": elapsed
        }

def collect_data_from_logs(log_directory):
    # read all log files and parse them
    all_records = []
    for filename in os.listdir(log_directory):
        if filename.endswith('_job_times.log'):
            file_path = os.path.join(log_directory, filename)
            record = parse_slurm_log(file_path)
            all_records.append(record)
    return all_records

def save_to_csv(records, output_file):
    # save as csv
    keys = records[0].keys()
    with open(output_file, 'w', newline='') as output:
        dict_writer = csv.DictWriter(output, keys)
        dict_writer.writeheader()
        dict_writer.writerows(records)

def save_to_json(records, output_file):
    # save as json
    with open(output_file, 'w') as output:
        json.dump(records, output, indent=4)

# Test
log_directory = '/path/to/log/files'
records = collect_data_from_logs(log_directory)
save_to_csv(records, 'slurm_records.csv')
save_to_json(records, 'slurm_records.json')