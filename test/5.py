import sys
import pickle
import pm4py
import re, os
dependency = int(sys.argv[2])
sign=int(sys.argv[1])
def find_file(dependency, filename):
    numbers = re.findall(r'\d+', dependency)
    processed_string = '-'.join(numbers)
    indices = (processed_string.split('-'))[::-1]
    for index in indices:
        full_path = os.path.join("/home/hr546787/Code_Parser/pkl/", filename + "_" + str(sign) + "_" + str(index) + ".pkl")
        if os.path.exists(full_path):
            return index


index=find_file(dependency,'c')
with open(f'/home/hr546787/Code_Parser/pkl/c_655973_{index}.pkl', 'rb') as f:
    c = pickle.load(f)

if c:
    a = 2
    job_index = int(sys.argv[3])
    with open(f'pkl/a_655973_{job_index}.pkl', 'wb') as f:
        pickle.dump(a, f)