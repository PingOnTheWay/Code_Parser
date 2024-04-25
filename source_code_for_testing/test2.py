import pm4py
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.importer.csv import importer as csv_importer
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.statistics.traces.log import case_statistics

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

# Step 5: Compute and display basic statistics about the process
general_stats = case_statistics.get_general_statistics(event_log)
print("General Stats:", general_stats)

# Optionally save the visualization as an image
pn_visualizer.save(gviz, "process_model.png")
