unique_activities = None
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
unique_activities = set()
with open(f'/home/hr546787/Code_Parser/pkl/unique_activities_{sign}.pkl', 'wb') as f:
    pickle.dump(unique_activities, f)
