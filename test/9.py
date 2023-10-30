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


i=float(sys.argv[4])


index=find_file(dependency, 'ping')
with open(f'/home/hr546787/Code_Parser/pkl/ping_655973_{index}.pkl', 'rb') as f:
    ping = pickle.load(f)

check = print(i, ping)