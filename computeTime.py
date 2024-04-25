from datetime import timedelta

def parse_time(s):
    h, m, s = map(int, s.split(':'))
    return timedelta(hours=h, minutes=m, seconds=s)

def average_time(file_path):
    times = {'start': [], 'step_0_0': [], 'step_1_10': [], 'compare':[], 'step_1_1':[], 'step_1_2':[], 'step_1_3':[], 'step_1_4':[], 'step_1_5':[], 'step_1_6':[], 'step_1_7':[], 'step_1_8':[], 'step_1_9':[]}

    with open(file_path, 'r') as f:
        for line in f:
            parts = line.split()
            job_type = parts[-1]
            elapsed_time = parts[-2]
            if job_type in times:
                times[job_type].append(parse_time(elapsed_time))

    averages = {}
    for job_type, elapsed_times in times.items():
        if elapsed_times:
            avg_time = sum(elapsed_times, timedelta()) / len(elapsed_times)
            averages[job_type] = avg_time

    return averages

# Replace 'your_file_path.txt' with the actual path to your text file
file_path = '/Users/pingwan/Desktop/Thesis_Project/Code_Parser/output/receipt3.log'
averages = average_time(file_path)

for job_type, avg_time in averages.items():
    print(f"Average elapsed time for {job_type}: {avg_time}")