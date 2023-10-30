import sys
import pickle
import pm4py
log = pm4py.read_xes('running-example.xes')
job_index=int(sys.argv[3])

with open(f'/home/hr546787/Code_Parser/pkl/log_655973_{job_index}.pkl', 'wb') as f:
    pickle.dump(log, f)
