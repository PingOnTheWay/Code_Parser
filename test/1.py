import sys
import pickle
import pm4py
noise_threshold=float(sys.argv[1])


with open('pkl/log.pkl', 'rb') as f:
    log = pickle.load(f)

(net, im, fm) = pm4py.discover_petri_net_inductive(log, noise_threshold=noise_threshold)
with open('pkl/net.pkl', 'wb') as f:
    pickle.dump(net, f)


with open('pkl/im.pkl', 'wb') as f:
    pickle.dump(im, f)


with open('pkl/fm.pkl', 'wb') as f:
    pickle.dump(fm, f)
