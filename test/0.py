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
log_csv = csv_importer.apply('your_log_file.csv')
parameters = {log_converter.Variants.TO_EVENT_LOG.value.Parameters.
    CASE_ID_KEY: 'case_id_column_name'}
event_log = log_converter.apply(log_csv, parameters=parameters, variant=
    log_converter.Variants.TO_EVENT_LOG)
net, initial_marking, final_marking = alpha_miner.apply(event_log)
gviz = pn_visualizer.apply(net, initial_marking, final_marking)
pn_visualizer.view(gviz)
with open(f'/home/hr546787/Code_Parser/pkl/parameters_{sign}.pkl', 'wb') as f:
    pickle.dump(parameters, f)
with open(f'/home/hr546787/Code_Parser/pkl/log_csv_{sign}.pkl', 'wb') as f:
    pickle.dump(log_csv, f)
with open(f'/home/hr546787/Code_Parser/pkl/event_log_{sign}.pkl', 'wb') as f:
    pickle.dump(event_log, f)
with open(f'/home/hr546787/Code_Parser/pkl/net_{sign}.pkl', 'wb') as f:
    pickle.dump(net, f)
with open(f'/home/hr546787/Code_Parser/pkl/initial_marking_{sign}.pkl', 'wb') as f:
    pickle.dump(initial_marking, f)
with open(f'/home/hr546787/Code_Parser/pkl/final_marking_{sign}.pkl', 'wb') as f:
    pickle.dump(final_marking, f)
with open(f'/home/hr546787/Code_Parser/pkl/gviz_{sign}.pkl', 'wb') as f:
    pickle.dump(gviz, f)
