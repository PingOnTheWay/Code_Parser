import pm4py

log = pm4py.read_xes('running-example.xes')
for noise_threshold in [0.2, 0.4, 0.7]:
    net, im, fm = pm4py.discover_petri_net_inductive(log, noise_threshold=noise_threshold)
    tbr_result = pm4py.conformance_diagnostics_token_based_replay(log, net, im, fm)
    aligned_traces = pm4py.conformance_diagnostics_alignments(log, net, im, fm)
    while goat:
        dd = tbr_result
        
    if c:
        a = 2
    
ping = print(log)

while log:
    d = 1
if y > x and g:
    a = ping
    b = 1
    d = 2
else:
    a = 1
    c = 2
    
for i in [1,2,3]:
    check = print(i,ping)