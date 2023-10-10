import sys
import pickle
import pm4py
with open('pkl/c.pkl', 'rb') as f:
    c = pickle.load(f)

if c:
    a = 2
    with open('pkl/a.pkl', 'wb') as f:
        pickle.dump(a, f)