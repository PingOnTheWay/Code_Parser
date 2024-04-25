import ast

# Provided code snippet
code_snippet = """
import pm4py

log = pm4py.read_xes('running-example.xes')
filter_log = pm4py.filtering.filter_log_variants_percentage(log, percentage=90)

for noise_threshold in [0.2, 0.4, 0.7]:
    net, im, fm = pm4py.discover_petri_net_inductive(filter_log, noise_threshold=noise_threshold)
    tbr_result = pm4py.conformance_diagnostics_token_based_replay(filter_log, net, im, fm)
    aligned_traces = pm4py.conformance_diagnostics_alignments(filter_log, net, im, fm)
"""

# Parse the code into an AST
parsed_ast = ast.parse(code_snippet)

# Function to analyze AST nodes and extract dependency information
def analyze_dependencies(node, dependency_dict, current_vars=set()):
    if isinstance(node, ast.Assign):
        # For Assign nodes, add the targets to the current variables
        for target in node.targets:
            if isinstance(target, ast.Name):
                current_vars.add(target.id)
                dependency_dict[target.id] = list(current_vars)
    elif isinstance(node, ast.For):
        # For For nodes, the target variable is added to the current variables
        if isinstance(node.target, ast.Name):
            current_vars.add(node.target.id)
            dependency_dict[node.target.id] = list(current_vars)
    elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
        # For Call nodes, add the function call as a dependency
        if isinstance(node.func.value, ast.Name):
            func_name = node.func.value.id + '.' + node.func.attr
            dependency_dict[func_name] = list(current_vars)
    
    # Recursively analyze child nodes
    for child in ast.iter_child_nodes(node):
        analyze_dependencies(child, dependency_dict, current_vars)

# Dictionary to hold the dependencies
dependencies = {}

# Analyze dependencies
analyze_dependencies(parsed_ast, dependencies)

# Dependencies now contain a mapping of variable and function calls to their dependencies
print(dependencies)


import networkx as nx
import matplotlib.pyplot as plt

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges based on the dependencies dictionary
for key, values in dependencies.items():
    G.add_node(key)
    for value in values:
        G.add_node(value)
        G.add_edge(value, key)

# Draw the graph
plt.figure(figsize=(12, 12))
nx.draw(G, with_labels=True, node_color='lightblue', font_weight='bold')
plt.show()