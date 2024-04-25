import ast
import graphviz

code_snippet = """
import pm4py

log = pm4py.read_xes('running-example.xes')
for noise_threshold in [0.2, 0.4, 0.7]:
    net, im, fm = pm4py.discover_petri_net_inductive(log, noise_threshold=noise_threshold)
    tbr_result = pm4py.conformance_diagnostics_token_based_replay(log, net, im, fm)
"""

parsed_ast = ast.parse(code_snippet)

def get_label(node):
    label = node.__class__.__name__
    if isinstance(node, ast.Name):
        label += f': {node.id}'
    elif isinstance(node, ast.Attribute):
        label += f': {node.attr}'
    elif isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            label += f': {node.func.id}'
        elif isinstance(node.func, ast.Attribute):
            label += f': {node.func.attr}'
    elif isinstance(node, ast.arg):
        label += f': {node.arg}'
    elif isinstance(node, ast.FunctionDef):
        label += f': {node.name}'
    elif isinstance(node, ast.ClassDef):
        label += f': {node.name}'
    elif isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):
                label += f': {target.id}'
    return label

def visualize_ast(node, graph=None, parent=None, name=''):
    if graph is None:
        graph = graphviz.Digraph('AST', node_attr={'shape': 'box', 'dpi': '300'}, format='png')
    label = get_label(node)
    graph.node(name, label)
    
    if parent is not None:
        graph.edge(parent, name)
    
    for index, child in enumerate(ast.iter_child_nodes(node)):
        child_name = f'{name}_{index}'
        visualize_ast(child, graph, name, child_name)
    
    return graph

ast_graph = visualize_ast(parsed_ast)
ast_graph.render('ast_graph_detailed', view=True, format='png')
