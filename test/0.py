log = None
import pm4py
import re, os, pickle, sys
sign = sys.argv[1]
log = pm4py.read_xes('running-example.xes')
with open(f'/home/hr546787/Code_Parser/pkl/log_{sign}.pkl', 'wb') as f:
    pickle.dump(log, f)
