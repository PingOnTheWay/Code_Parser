import sys
import pickle
import pm4py
with open('pkl/log.pkl', 'rb') as f:
    log = pickle.load(f)

while log:
    d = 1
with open('pkl/d.pkl', 'wb') as f:
    pickle.dump(d, f)