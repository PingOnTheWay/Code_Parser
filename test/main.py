import pm4py

log = pm4py.read_xes('running-example.xes')

print("Original log size: ")

for noise_threshold in [0.2, 0.4, 0.7]:
    net, im, fm = pm4py.discover_petri_net_inductive(log, noise_threshold=noise_threshold)
    tbr_result = pm4py.conformance_diagnostics_token_based_replay(log, net, im, fm)
    aligned_traces = pm4py.conformance_diagnostics_alignments(log, net, im, fm)
    lang_fit = pm4py.fitness_token_based_replay(log, net, im, fm)
    
