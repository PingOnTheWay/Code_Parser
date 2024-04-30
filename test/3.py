average_duration = None
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

if case_durations:
    average_duration = np.mean([d.total_seconds() for d in case_durations])
    print(f'Average Case Duration: {average_duration / 3600} hours')
with open(f'/home/hr546787/Code_Parser/pkl/average_duration_{sign}.pkl', 'wb') as f:
    pickle.dump(average_duration, f)
