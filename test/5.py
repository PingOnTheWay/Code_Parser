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
average_durations = {activity: np.mean(durations) for activity, durations in
    activity_durations.items()}
print('Average Durations per Activity:', average_durations)
with open(f'/home/hr546787/Code_Parser/pkl/average_durations_{sign}.pkl', 'wb') as f:
    pickle.dump(average_durations, f)
