import sys
import pickle
import pm4py
with open('pkl/goat.pkl', 'rb') as f:
    goat = pickle.load(f)


with open('pkl/tbr_result.pkl', 'rb') as f:
    tbr_result = pickle.load(f)

while goat:
    dd = tbr_result
with open('pkl/dd.pkl', 'wb') as f:
    pickle.dump(dd, f)