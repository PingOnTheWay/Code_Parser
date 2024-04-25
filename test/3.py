import pm4py

from pm4py.objects.conversion.log import converter as log_converter

from pm4py.objects.log.importer.csv import importer as csv_importer

from pm4py.algo.discovery.alpha import algorithm as alpha_miner

from pm4py.visualization.petri_net import visualizer as pn_visualizer

from pm4py.util import constants

from pm4py.statistics.traces.log import case_statistics

from pm4py.statistics.performance_spectrum import algorithm as performance_spectrum_algo

from pm4py.visualization.performance_spectrum import visualizer as performance_spectrum_visualizer

from datetime import timedelta

import numpy as np
import re, os, pickle, sys
sign = sys.argv[1]
with open(f'/home/hr546787/Code_Parser/pkl/activity_counts_{sign}.pkl', 'rb') as f:
    activity_counts = pickle.load(f)

with open(f'/home/hr546787/Code_Parser/pkl/constants_{sign}.pkl', 'rb') as f:
    constants = pickle.load(f)

with open(f'/home/hr546787/Code_Parser/pkl/event_log_{sign}.pkl', 'rb') as f:
    event_log = pickle.load(f)

with open(f'/home/hr546787/Code_Parser/pkl/len_{sign}.pkl', 'rb') as f:
    len = pickle.load(f)

with open(f'/home/hr546787/Code_Parser/pkl/event_index_{sign}.pkl', 'rb') as f:
    event_index = pickle.load(f)

with open(f'/home/hr546787/Code_Parser/pkl/activity_durations_{sign}.pkl', 'rb') as f:
    activity_durations = pickle.load(f)

trace_index = float(sys.argv[3])
if trace_index < len(event_log):
    trace = event_log[trace_index]
    for event_index in range(len(trace) - 1):
        start_event = trace[event_index]
        end_event = trace[event_index + 1]
        duration = (end_event[constants.PARAMETER_CONSTANT_TIMESTAMP_KEY] -
            start_event[constants.PARAMETER_CONSTANT_TIMESTAMP_KEY]
            ).total_seconds()
        activity_name = start_event['concept:name']
        if activity_name not in activity_durations:
            activity_durations[activity_name] = []
        activity_durations[activity_name].append(duration)
        if activity_name not in activity_counts:
            activity_counts[activity_name] = 0
        activity_counts[activity_name] += 1
with open(f'/home/hr546787/Code_Parser/pkl/activity_name_{sign}.pkl', 'wb') as f:
    pickle.dump(activity_name, f)
with open(f'/home/hr546787/Code_Parser/pkl/duration_{sign}.pkl', 'wb') as f:
    pickle.dump(duration, f)
with open(f'/home/hr546787/Code_Parser/pkl/end_event_{sign}.pkl', 'wb') as f:
    pickle.dump(end_event, f)
with open(f'/home/hr546787/Code_Parser/pkl/start_event_{sign}.pkl', 'wb') as f:
    pickle.dump(start_event, f)
with open(f'/home/hr546787/Code_Parser/pkl/trace_{sign}.pkl', 'wb') as f:
    pickle.dump(trace, f)
