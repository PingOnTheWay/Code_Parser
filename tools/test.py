import ast

class IfConditionVariableCollector(ast.NodeVisitor):
    def __init__(self):
        self.variables = []

    def visit_Name(self, node):
        self.variables.append(node.id)

def collect_if_condition_variables(code):
    tree = ast.parse(code)
    collector = IfConditionVariableCollector()
    
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            # 仅遍历 if 条件部分
            collector.visit(node.test)
    
    return collector.variables

# 示例
code = """
if x > 10 and y < 20:
    result = z + w
    print(a, b)
elif ping >30:
    print(b)
"""

variables = collect_if_condition_variables(code)
print(variables)  # ['x', 'y']

# Import some libraries that i need
import_libaries = "import sys\nimport pickle\n"

import_nodes = []
assign_nodes = []
forloop_nodes = []
if_nodes = []
while_nodes = []
tree_nodes =[]

def parse_assign_node(assign_node):
    # Parse targets
    targets=[]
    for target in assign_node.targets:
        if isinstance(target, ast.Name):
                targets.append(target.id)
        elif isinstance(target, ast.Tuple):
            for elt in target.elts:
                if isinstance(elt, ast.Name):
                    targets.append(elt.id)
    # Initialize args and keywords
    dependences = []
    # Parse args and keywords if value is a Call node
    if isinstance(assign_node.value, ast.Call):
        dependences = [arg.id if isinstance(arg, ast.Name) else arg.value for arg in assign_node.value.args]
        dependences += [keyword.value.id if isinstance(keyword.value, ast.Name) else keyword.value.value for keyword in assign_node.value.keywords]
    elif isinstance(assign_node.value, ast.Name):
        dependences.append(assign_node.value.id)    
    return {
        'targets': targets,
        'dependences': dependences,
        'lineno': assign_node.lineno
    }

def parse_node(node, index, parent=None):
    # print(ast.dump(ast_tree, indent=2))
    for child in ast.iter_child_nodes(node):
        if isinstance(child, ast.Import):
            import_nodes.append(child)
        elif isinstance(child, ast.Assign):
            assign_nodes.append(child)
            tree_nodes.append(child)
            generate_python_script(child, index, parent)
            index += 1
        elif isinstance(child, ast.For):
            forloop_nodes.append(child)
            tree_nodes.append(child)
            parse_for_node(child, index)
        elif isinstance(child, ast.If):
            if_nodes.append(child)
            tree_nodes.append(child)
        elif isinstance(child, ast.While):
            while_nodes.append(child)
            tree_nodes.append(child)
            
def parse_for_node(node, index):
    parse_node(node, index, node)

def unparse_code(nodes):
    return ast.unparse(ast.Module(body=nodes, type_ignores=[]))

def generate_pickle_code_for_ouput(node):
    generated_code = []
    parsed_node = parse_assign_node(node)
    for ele in parsed_node['targets']:
        generated_code.append(f"\nwith open('pkl/{ele}.pkl', 'wb') as f:\n    pickle.dump({ele}, f)\n")
    return generated_code

def generate_pickle_code_for_input(node, parent):
    generated_code = []
    parsed_node = parse_assign_node(node)
    loop_variable = ''
    variables = []
    if parent is not None:
        loop_variable = parent.target.id
    for ele in parsed_node['dependences']:
        if ele != loop_variable:
            variables.append(ele)
        else:
            generated_code.append(f"\n{loop_variable}=float(sys.argv[1])\n")
     
    variables = list(set(variables))
    for var in variables:
        generated_code.append(f"\nwith open('pkl/{var}.pkl', 'rb') as f:\n    {var} = pickle.load(f)\n")
    return generated_code
            
def generate_python_script(node, index, parent):
    code = ''
    if index == 0:
        code = unparse_code(import_nodes + [node]) + '\n'.join(generate_pickle_code_for_ouput(node))
    else:
        code = unparse_code(import_nodes)+ '\n'.join(generate_pickle_code_for_input(node,parent)) + '\n'+ unparse_code([node])\
               + '\n'.join(generate_pickle_code_for_ouput(node))
    with open("test/" + str(index) + ".py", "w") as f:
        f.write(import_libaries + code)
    


code = '''
import pm4py

log = pm4py.read_xes('running-example.xes')
for noise_threshold in [0.2, 0.4, 0.7]:
    net, im, fm = pm4py.discover_petri_net_inductive(log, noise_threshold=noise_threshold)
    tbr_result = pm4py.conformance_diagnostics_token_based_replay(log, net, im, fm)
    aligned_traces = pm4py.conformance_diagnostics_alignments(log, net, im, fm)
    
ping = log 
'''
parse_node(ast.parse(code), 0)
print(import_nodes)
print(assign_nodes)
print(forloop_nodes)
print(while_nodes)