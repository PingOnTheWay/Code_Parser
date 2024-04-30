aligned_traces = None
lang_fit = None
fm = None
im = None
net = None
tbr_result = None
import pm4py
import re, os, pickle, sys
sign = sys.argv[1]
with open(f'/home/hr546787/Code_Parser/pkl/log_{sign}.pkl', 'rb') as f:
    log = pickle.load(f)

noise_threshold = float(sys.argv[3])
net, im, fm = pm4py.discover_petri_net_inductive(log, noise_threshold=
    noise_threshold)
tbr_result = pm4py.conformance_diagnostics_token_based_replay(log, net, im, fm)
aligned_traces = pm4py.conformance_diagnostics_alignments(log, net, im, fm)
lang_fit = pm4py.fitness_token_based_replay(log, net, im, fm)
with open(f'/home/hr546787/Code_Parser/pkl/aligned_traces_{sign}.pkl', 'wb') as f:
    pickle.dump(aligned_traces, f)
with open(f'/home/hr546787/Code_Parser/pkl/lang_fit_{sign}.pkl', 'wb') as f:
    pickle.dump(lang_fit, f)
with open(f'/home/hr546787/Code_Parser/pkl/fm_{sign}.pkl', 'wb') as f:
    pickle.dump(fm, f)
with open(f'/home/hr546787/Code_Parser/pkl/im_{sign}.pkl', 'wb') as f:
    pickle.dump(im, f)
with open(f'/home/hr546787/Code_Parser/pkl/net_{sign}.pkl', 'wb') as f:
    pickle.dump(net, f)
with open(f'/home/hr546787/Code_Parser/pkl/tbr_result_{sign}.pkl', 'wb') as f:
    pickle.dump(tbr_result, f)
