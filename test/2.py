import sys
import pickle
import pm4py
with open('pkl/im.pkl', 'rb') as f:
    im = pickle.load(f)


with open('pkl/fm.pkl', 'rb') as f:
    fm = pickle.load(f)


with open('pkl/log.pkl', 'rb') as f:
    log = pickle.load(f)


with open('pkl/net.pkl', 'rb') as f:
    net = pickle.load(f)

tbr_result = pm4py.conformance_diagnostics_token_based_replay(log, net, im, fm)
with open('pkl/tbr_result.pkl', 'wb') as f:
    pickle.dump(tbr_result, f)
