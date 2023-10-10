import sys
import pickle
import pm4py
i=float(sys.argv[1])


with open('pkl/ping.pkl', 'rb') as f:
    ping = pickle.load(f)

check = print(i, ping)