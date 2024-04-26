import os
import csv

# Define the directory containing log files (this will be user-defined in actual usage)
log_directory = input("Please enter the directory containing log files: ")

# Prepare the output CSV file
csv_filename = os.path.join(log_directory, "process_mining_data.csv")

with open(csv_filename, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    # Write the header row
    csv_writer.writerow(['case_id', 'activity', 'timestamp', 'cost'])

    # Loop through all files in the directory
    for filename in os.listdir(log_directory):
        if filename.endswith(".log"):
            # Split the filename to extract case ID and activity
            parts = filename.split('_')
            case_id = parts[0]
            activity = parts[1].split('.')[0]  # Remove the .log extension
            
            # Read the timestamp and cost from the file
            with open(os.path.join(log_directory, filename), 'r') as file:
                lines = file.readlines()
                # Assuming the required data is on the third line, as per the provided example
                data_parts = lines[2].split()
                timestamp = data_parts[1]
                cost = data_parts[3].split(":")[-1]  # Extract seconds for the cost

            # Write the data to the CSV file
            csv_writer.writerow([case_id, activity, timestamp, cost])

print(f"Process mining data has been written to {csv_filename}")

import pandas as pd
import pm4py
from pm4py.objects.log.util import dataframe_utils
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.visualization.petri_net import visualizer as pn_visualizer

dataframe = pd.read_csv(csv_filename, sep=',')
activity_costs = dataframe.groupby('activity')['cost'].mean().round(2).to_dict()

dataframe = dataframe_utils.convert_timestamp_columns_in_df(dataframe)
dataframe = pm4py.format_dataframe(dataframe, case_id='case_id', activity_key='activity', timestamp_key='timestamp')
event_log = pm4py.convert_to_event_log(dataframe)

net, im, fm = pm4py.discover_petri_net_inductive(event_log)

for transition in net.transitions:
    if transition.label is not None:
        if transition.label in activity_costs:
            transition.label = f"{transition.label} (avg_cost: {activity_costs[transition.label]})"

parameters = {pn_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: "png"}
gviz = pn_visualizer.apply(net, im, fm, parameters=parameters)
pn_visualizer.save(gviz, log_directory + '/petri_net_with_cost.png')
pn_visualizer.view(gviz)