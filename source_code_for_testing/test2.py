import pm4py
import pandas as pd
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.statistics.traces.generic.log import case_statistics

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

# Step 5: Compute and display basic statistics about the process
general_stats = case_statistics.get_variant_statistics(event_log)
print("General Stats:", general_stats)

# Optionally save the visualization as an image
pn_visualizer.save(gviz, "process_model.png")