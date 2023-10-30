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


index=find_file(dependency,'x')
with open(f'/home/hr546787/Code_Parser/pkl/x_655973_{index}.pkl', 'rb') as f:
    x = pickle.load(f)


index=find_file(dependency,'ping')
with open(f'/home/hr546787/Code_Parser/pkl/ping_655973_{index}.pkl', 'rb') as f:
    ping = pickle.load(f)


index=find_file(dependency,'y')
with open(f'/home/hr546787/Code_Parser/pkl/y_655973_{index}.pkl', 'rb') as f:
    y = pickle.load(f)


index=find_file(dependency,'g')
with open(f'/home/hr546787/Code_Parser/pkl/g_655973_{index}.pkl', 'rb') as f:
    g = pickle.load(f)

if y > x and g:
    a = ping
    b = 1
    d = 2
    job_index = int(sys.argv[3])
    with open(f'pkl/a_655973_{job_index}.pkl', 'wb') as f:
        pickle.dump(a, f)
    job_index = int(sys.argv[3])
    with open(f'pkl/b_655973_{job_index}.pkl', 'wb') as f:
        pickle.dump(b, f)
    job_index = int(sys.argv[3])
    with open(f'pkl/d_655973_{job_index}.pkl', 'wb') as f:
        pickle.dump(d, f)
else:
    a = 1
    c = 2
    job_index = int(sys.argv[3])
    with open(f'pkl/a_655973_{job_index}.pkl', 'wb') as f:
        pickle.dump(a, f)
    job_index = int(sys.argv[3])
    with open(f'pkl/c_655973_{job_index}.pkl', 'wb') as f:
        pickle.dump(c, f)