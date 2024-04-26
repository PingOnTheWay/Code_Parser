case = None
case_duration = None
case_index = None
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
with open(f'/home/hr546787/Code_Parser/pkl/case_durations_{sign}.pkl', 'rb') as f:
    case_durations = pickle.load(f)

with open(f'/home/hr546787/Code_Parser/pkl/event_log_{sign}.pkl', 'rb') as f:
    event_log = pickle.load(f)

case_index = float(sys.argv[3])
case_index = int(case_index)
if case_index < len(event_log):
    case = event_log[case_index]
    case_duration = case[-1]['time:timestamp'] - case[0]['time:timestamp']
    case_durations.append(case_duration)
    print(f"Case {case.attributes['concept:name']} duration: {case_duration}")
with open(f'/home/hr546787/Code_Parser/pkl/case_{sign}.pkl', 'wb') as f:
    pickle.dump(case, f)
with open(f'/home/hr546787/Code_Parser/pkl/case_duration_{sign}.pkl', 'wb') as f:
    pickle.dump(case_duration, f)
with open(f'/home/hr546787/Code_Parser/pkl/case_index_{sign}.pkl', 'wb') as f:
    pickle.dump(case_index, f)
