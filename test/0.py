import sys
import pickle
import pm4py
log = pm4py.read_xes('running-example.xes')
with open('pkl/log.pkl', 'wb') as f:
    pickle.dump(log, f)
