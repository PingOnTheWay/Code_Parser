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

aligned_traces = pm4py.conformance_diagnostics_alignments(log, net, im, fm)
with open('pkl/aligned_traces.pkl', 'wb') as f:
    pickle.dump(aligned_traces, f)
