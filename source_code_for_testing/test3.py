import pm4py
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.importer.csv import importer as csv_importer
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.statistics.traces.log import case_statistics
from pm4py.util import constants
from pm4py.statistics.start_activities.log import get as start_activities
from pm4py.statistics.end_activities.log import get as end_activities
from datetime import timedelta
import numpy as np

# Step 1: Import data from a CSV file
log_csv = csv_importer.apply('your_log_file.csv')

# Step 2: Convert the CSV data to an event log object
parameters = {
    log_converter.Variants.TO_EVENT_LOG.value.Parameters.CASE_ID_KEY: 'case_id_column_name'
}
event_log = log_converter.apply(log_csv, parameters=parameters, variant=log_converter.Variants.TO_EVENT_LOG)

# Step 3: Discover a process model using Alpha Miner
net, initial_marking, final_marking = alpha_miner.apply(event_log)

# Step 4: Visualize the process model
gviz = pn_visualizer.apply(net, initial_marking, final_marking)
pn_visualizer.view(gviz)

# Additional Task 1: Calculate duration for each case (limited to first 5 cases for example)
case_durations = []
for case_index in [0, 1, 2, 3, 4]:
    if case_index < len(event_log):
        case = event_log[case_index]
        case_duration = case[-1][constants.PARAMETER_CONSTANT_TIMESTAMP_KEY] - case[0][constants.PARAMETER_CONSTANT_TIMESTAMP_KEY]
        case_durations.append(case_duration)
        print(f"Case {case.attributes['concept:name']} duration: {case_duration}")

# Average case duration
if case_durations:
    average_duration = np.mean(case_durations)
    print(f"Average Case Duration: {average_duration}")

# Additional Task 2: Identify and print all unique activities (limited to first 5 traces)
unique_activities = set()
for trace_index in [0, 1, 2, 3, 4]:
    if trace_index < len(event_log):
        trace = event_log[trace_index]
        for event in trace:
            unique_activities.add(event['concept:name'])
print("Unique Activities:", unique_activities)

# Additional Task 3: Count and print frequency of each activity (limited to first 5 traces)
activity_frequency = {}
for trace_index in [0, 1, 2, 3, 4]:
    if trace_index < len(event_log):
        trace = event_log[trace_index]
        for event in trace:
            activity = event['concept:name']
            if activity not in activity_frequency:
                activity_frequency[activity] = 0
            activity_frequency[activity] += 1
print("Activity Frequency:", activity_frequency)

# Optionally save the visualization as an image
pn_visualizer.save(gviz, "process_model.png")