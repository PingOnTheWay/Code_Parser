import sys
import pickle
import pm4py
with open('pkl/ping.pkl', 'rb') as f:
    ping = pickle.load(f)


with open('pkl/g.pkl', 'rb') as f:
    g = pickle.load(f)


with open('pkl/x.pkl', 'rb') as f:
    x = pickle.load(f)


with open('pkl/y.pkl', 'rb') as f:
    y = pickle.load(f)

if y > x and g:
    a = ping
    b = 1
    d = 2
    with open('pkl/d.pkl', 'wb') as f:
        pickle.dump(d, f)
    with open('pkl/a.pkl', 'wb') as f:
        pickle.dump(a, f)
    with open('pkl/b.pkl', 'wb') as f:
        pickle.dump(b, f)
else:
    a = 1
    c = 2
    with open('pkl/a.pkl', 'wb') as f:
        pickle.dump(a, f)
    with open('pkl/c.pkl', 'wb') as f:
        pickle.dump(c, f)