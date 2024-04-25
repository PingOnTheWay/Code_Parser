import pm4py
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.visualization.petri_net import visualizer as pn_visualizer

log_path = '/Users/pingwan/Desktop/Thesis_Project/Code_Parser/output/event1.xes'

import pm4py
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.visualization.process_tree import visualizer as pt_visualizer

log = pm4py.read_xes(log_path)

net, im, fm = pm4py.discover_petri_net_inductive(log)

gviz = pn_visualizer.apply(net, im, fm, parameters={pn_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: "png"})
pn_visualizer.view(gviz)