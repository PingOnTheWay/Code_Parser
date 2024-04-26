dataframe = None
net = None
initial_marking = None
gviz = None
final_marking = None
event_log = None
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
dataframe = pd.read_csv('event_log/Sample_Process_Mining.csv', sep=',')
dataframe = pm4py.format_dataframe(dataframe, case_id='case_id',
    activity_key='activity', timestamp_key='timestamp')
event_log = pm4py.convert_to_event_log(dataframe)
net, initial_marking, final_marking = alpha_miner.apply(event_log)
gviz = pn_visualizer.apply(net, initial_marking, final_marking)
pn_visualizer.view(gviz)
with open(f'/home/hr546787/Code_Parser/pkl/dataframe_{sign}.pkl', 'wb') as f:
    pickle.dump(dataframe, f)
with open(f'/home/hr546787/Code_Parser/pkl/net_{sign}.pkl', 'wb') as f:
    pickle.dump(net, f)
with open(f'/home/hr546787/Code_Parser/pkl/initial_marking_{sign}.pkl', 'wb') as f:
    pickle.dump(initial_marking, f)
with open(f'/home/hr546787/Code_Parser/pkl/gviz_{sign}.pkl', 'wb') as f:
    pickle.dump(gviz, f)
with open(f'/home/hr546787/Code_Parser/pkl/final_marking_{sign}.pkl', 'wb') as f:
    pickle.dump(final_marking, f)
with open(f'/home/hr546787/Code_Parser/pkl/event_log_{sign}.pkl', 'wb') as f:
    pickle.dump(event_log, f)
