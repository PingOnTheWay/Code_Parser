trace = None
trace_index = None
import pm4py

import pandas as pd

from pm4py.objects.conversion.log import converter as log_converter

from pm4py.algo.discovery.alpha import algorithm as alpha_miner

from pm4py.visualization.petri_net import visualizer as pn_visualizer

from pm4py.util import constants

from pm4py.statistics.start_activities.log import get as start_activities

from pm4py.statistics.end_activities.log import get as end_activities

from datetime import timedelta

import numpy as np
import re, os, pickle, sys
sign = sys.argv[1]
with open(f'/home/hr546787/Code_Parser/pkl/event_log_{sign}.pkl', 'rb') as f:
    event_log = pickle.load(f)

with open(f'/home/hr546787/Code_Parser/pkl/unique_activities_{sign}.pkl', 'rb') as f:
    unique_activities = pickle.load(f)

trace_index = float(sys.argv[3])
trace_index = int(trace_index)
if trace_index < len(event_log):
    trace = event_log[trace_index]
    for event in trace:
        unique_activities.add(event['concept:name'])
with open(f'/home/hr546787/Code_Parser/pkl/trace_{sign}.pkl', 'wb') as f:
    pickle.dump(trace, f)
with open(f'/home/hr546787/Code_Parser/pkl/trace_index_{sign}.pkl', 'wb') as f:
    pickle.dump(trace_index, f)
