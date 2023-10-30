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


index=find_file(dependency, 'im')
with open(f'/home/hr546787/Code_Parser/pkl/im_655973_{index}.pkl', 'rb') as f:
    im = pickle.load(f)


index=find_file(dependency, 'log')
with open(f'/home/hr546787/Code_Parser/pkl/log_655973_{index}.pkl', 'rb') as f:
    log = pickle.load(f)


index=find_file(dependency, 'net')
with open(f'/home/hr546787/Code_Parser/pkl/net_655973_{index}.pkl', 'rb') as f:
    net = pickle.load(f)


index=find_file(dependency, 'fm')
with open(f'/home/hr546787/Code_Parser/pkl/fm_655973_{index}.pkl', 'rb') as f:
    fm = pickle.load(f)

aligned_traces = pm4py.conformance_diagnostics_alignments(log, net, im, fm)
job_index=int(sys.argv[3])

with open(f'/home/hr546787/Code_Parser/pkl/aligned_traces_655973_{job_index}.pkl', 'wb') as f:
    pickle.dump(aligned_traces, f)
