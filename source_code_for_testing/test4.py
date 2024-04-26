import pm4py
import pandas as pd
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.util import constants
from pm4py.statistics.traces.generic.log import case_statistics
from pm4py.algo.discovery.performance_spectrum.variants.dataframe import apply
from pm4py.visualization.performance_spectrum import visualizer as performance_spectrum_visualizer
from datetime import timedelta
import numpy as np

# Step 1: Import data from a CSV file
dataframe = pd.read_csv('event_log/Sample_Process_Mining.csv', sep=',')

# Step 2: Convert the CSV data to an event log object
dataframe = pm4py.format_dataframe(dataframe, case_id='case_id', activity_key='activity', timestamp_key='timestamp')
event_log = pm4py.convert_to_event_log(dataframe)

# Step 3: Discover a process model using Alpha Miner
net, initial_marking, final_marking = alpha_miner.apply(event_log)

# Step 4: Visualize the process model
gviz = pn_visualizer.apply(net, initial_marking, final_marking)
pn_visualizer.view(gviz)

# Additional Task 1: Compute average duration for each activity type
activity_durations = {}
activity_counts = {}
for trace_index in [0, 1, 2, 3, 4]:  # Static loop structure
    trace_index = int(trace_index)
    if trace_index < len(event_log):
        trace = event_log[trace_index]
        for event_index in range(len(trace) - 1):
            start_event = trace[event_index]
            end_event = trace[event_index + 1]
            duration = (end_event['time:timestamp'] - start_event['time:timestamp']).total_seconds()
            activity_name = start_event['concept:name']
            if activity_name not in activity_durations:
                activity_durations[activity_name] = []
            activity_durations[activity_name].append(duration)
            if activity_name not in activity_counts:
                activity_counts[activity_name] = 0
            activity_counts[activity_name] += 1

# Calculate average durations
average_durations = {activity: np.mean(durations) for activity, durations in activity_durations.items()}
print("Average Durations per Activity:", average_durations)

# Additional Task 2: Visualize the performance spectrum
if len(event_log) > 5:
    performance_log = pm4py.filter_log(lambda x: x.attributes['concept:name'] in set(event_log[i].attributes['concept:name'] for i in [0, 1, 2, 3, 4]), event_log)
    performance_spectrum = apply(performance_log)
    perf_gviz = performance_spectrum_visualizer.apply(performance_spectrum)
    performance_spectrum_visualizer.view(perf_gviz)

# Optionally save the visualization as an image
pn_visualizer.save(gviz, "process_model.png")
