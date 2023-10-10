import sys
import pickle
import pm4py
with open('pkl/log.pkl', 'rb') as f:
    log = pickle.load(f)

ping = print(log)
with open('pkl/ping.pkl', 'wb') as f:
    pickle.dump(ping, f)
