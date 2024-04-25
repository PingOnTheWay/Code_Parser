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
with open(f'/home/hr546787/Code_Parser/pkl/performance_spectrum_visualizer_{sign}.pkl', 'rb') as f:
    performance_spectrum_visualizer = pickle.load(f)

with open(f'/home/hr546787/Code_Parser/pkl/event_log_{sign}.pkl', 'rb') as f:
    event_log = pickle.load(f)

with open(f'/home/hr546787/Code_Parser/pkl/x_{sign}.pkl', 'rb') as f:
    x = pickle.load(f)

with open(f'/home/hr546787/Code_Parser/pkl/pm4py_{sign}.pkl', 'rb') as f:
    pm4py = pickle.load(f)

with open(f'/home/hr546787/Code_Parser/pkl/i_{sign}.pkl', 'rb') as f:
    i = pickle.load(f)

with open(f'/home/hr546787/Code_Parser/pkl/len_{sign}.pkl', 'rb') as f:
    len = pickle.load(f)

with open(f'/home/hr546787/Code_Parser/pkl/performance_spectrum_algo_{sign}.pkl', 'rb') as f:
    performance_spectrum_algo = pickle.load(f)

if len(event_log) > 5:
    performance_log = pm4py.filter_log(lambda x: x.attributes[
        'concept:name'] in set(event_log[i].attributes['concept:name'] for
        i in [0, 1, 2, 3, 4]), event_log)
    performance_spectrum = performance_spectrum_algo.apply(performance_log,
        parameters={performance_spectrum_algo.Parameters.ACTIVITY_KEY:
        'concept:name'})
    perf_gviz = performance_spectrum_visualizer.apply(performance_spectrum)
    performance_spectrum_visualizer.view(perf_gviz)
with open(f'/home/hr546787/Code_Parser/pkl/performance_spectrum_{sign}.pkl', 'wb') as f:
    pickle.dump(performance_spectrum, f)
with open(f'/home/hr546787/Code_Parser/pkl/perf_gviz_{sign}.pkl', 'wb') as f:
    pickle.dump(perf_gviz, f)
with open(f'/home/hr546787/Code_Parser/pkl/performance_log_{sign}.pkl', 'wb') as f:
    pickle.dump(performance_log, f)
