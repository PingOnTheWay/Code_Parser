import ast
import sys
sys.path.append("/Users/pingwan/Desktop/Thesis_Project/Code_Parser")
import tools.ScriptsGenerator as SG
import copy
from collections import defaultdict
import random
import re

# Import some libraries that i need
import_libaries = "import sys\nimport pickle\n"

# Initialize empty lists to collect relevant AST nodes
import_nodes = []
assign_nodes = []
tree_nodes = []

forloop_nodes = []
loops = []
if_while_nodes = []
sign = random.randint(10000, 1000000)

# Function to extract numbers from a string
def extract_numbers(s):
    numbers = re.findall(r'\d+', s)
    return '-'.join(numbers)

# Class to represent a loop
class Loop(ast.NodeVisitor):
    def __init__(self, lineno:int, end_lineno:int, variable:str, values:list) -> None:
        self.lineno = lineno
        self.end_lineno = end_lineno
        self.variable = variable
        self.values = values
        
    def __repr__(self) -> str:
        return f"Loop(lineno={self.lineno}, end_lineno={self.end_lineno}, variable={self.variable}, values={self.values})"
    
    def __lt__(self, other: 'Loop') -> bool:
        if not isinstance(other, Loop):
            return NotImplemented
        return self.lineno < other.lineno

    def __gt__(self, other: 'Loop') -> bool:
        if not isinstance(other, Loop):
            return NotImplemented
        return self.lineno > other.lineno

    def __eq__(self, other: 'Loop') -> bool:
        if not isinstance(other, Loop):
            return NotImplemented
        return self.lineno == other.lineno

# Sort Function used to arrange ast nodes according to the row number from small to large
def sort_nodes_by_lineno(nodes):
    return sorted(nodes, key=lambda node: node.lineno if hasattr(node, 'lineno') else float('inf'), reverse=False)

# Function to read a file as a string
def read_as_string(file_path):
    with open(file_path) as file:
        return file.read()
    
# Function to parse the code
# Three lists are used to store the import, assign and tree nodes respectively
def parse_code(file_path):
    code = read_as_string(file_path)
    ast_tree = ast.parse(code)
    for node in ast_tree.body:
        if isinstance(node, ast.Import):
            import_nodes.append(node)
        elif isinstance(node, ast.Assign):
            assign_nodes.append(node)
            tree_nodes.append(node)
        elif isinstance(node, ast.For):
            for subnode in node.body:
                if isinstance(subnode, (ast.Assign,ast.If,ast.While)):
                    assign_nodes.append(subnode)
            loops.append(Loop(node.lineno, node.end_lineno,node.target.id,[constant.value for constant in node.iter.elts]))
            forloop_nodes.append(node)
            tree_nodes.append(node)
        elif isinstance(node, (ast.If, ast.While)):
            # we can process if or while node as same as an assign node
            assign_nodes.append(node)
            if_while_nodes.append(node)
            
def parse_assign_node(assign_node, index):
    # Parse targets
    if isinstance(assign_node, (ast.While, ast.If)):
        dependences, if_vars, orelse_vars = extract_variables_from_code(assign_node)
        dependences = list(dependences)
        if_vars |= orelse_vars
        targets = list(if_vars)
    else:
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
        'lineno': assign_node.lineno,
        'file_name': index
    }
    
def build_dependency_tree(list_for_dependency):
    # Initialize a tree as a defaultdict
    for entry in list_for_dependency:
        print(entry)
    tree = defaultdict(list)

    # Create a lookup dictionary from targets to file_name
    target_to_file = {}
    for entry in list_for_dependency:
        for target in entry['targets']:
            target_to_file[target] = entry['file_name']

    # Build the tree based on dependencies
    for entry in list_for_dependency:
        for dep in entry['dependences']:
            if dep in target_to_file:
                parent = target_to_file[dep]
                child = entry['file_name']
                if child not in tree[parent]:  # Avoid duplicate children
                    tree[parent].append(child)
    tree = dict(tree)
    # Remove self-dependencies
    tree = {k: v for k, v in tree.items() if not (len(v) == 1 and v[0] == k)}
    # Initialize an empty set to keep track of visited nodes
    visited = set()

    # Iterate over each parent node in reversed order
    for parent in reversed(sorted(tree.keys())):
        # Filter out nodes that have been visited
        tree[parent] = [child for child in tree[parent] if child not in visited]
        # Update the visited set
        visited.update(tree[parent])
    return tree

def generate_scripts(nodes):
    index = 0
    pos = ''
    list_for_dependency = []
    for node in sort_nodes_by_lineno(nodes):
        if index == 0:
            pos = 'start'
        elif index == len(nodes) - 1:
            pos = 'end'
        else:
            pos = ''
        arr = []
        arr.append(node)
        if isinstance(node, ast.Assign):
            # generate_python_script(arr, str(index), pos)
            variable = check_child_node_type(node)
            SG.generate_python_script(import_nodes, arr, str(index), sign, variable, pos)
        elif isinstance(node, (ast.If, ast.While)):
            variable, targets, orelse_targets = extract_variables_from_code(node)
            input_codes = SG.generate_input_code(variable, sign)
            new_node = process_node(node, targets, orelse_targets)
            new_node = ast.fix_missing_locations(new_node)
            with open("test/" + str(index) + ".py", "w") as f:
                code = SG.unparse_code(import_nodes) + '\n'.join(input_codes) +'\n' +SG.unparse_code([new_node])
                f.write(import_libaries + code)
        list_for_dependency.append(parse_assign_node(node, str(index)))
        # generate_slurm_script(str(index))
        index += 1
    # print(list_for_dependency)
    tree = build_dependency_tree(list_for_dependency)
    print(tree)
    file_with_dependency = set(tree.keys())
    for key in tree.keys():
        file_with_dependency |= set(tree[key])
    func(list_for_dependency,tree, '0')
    global job_index
    for file_name in range(1, index):
        if not str(file_name) in file_with_dependency:
            job_index += 1
            func(list_for_dependency,tree, str(file_name))
    
    # print(slurm_script_for_all)
    
def generate_slurm_script(file_name):
    slurm_script = '''#!/usr/local_rwth/bin/zsh
#SBATCH --mem-per-cpu=6G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1

export LD_LIBRARY_PATH="/usr/local_rwth/sw/python/3.8.7/x86_64/lib/:${LD_LIBRARY_PATH}"
srun /usr/local_rwth/sw/python/3.8.7/x86_64/bin/python3.8 '''
    slurm_script += f'/home/hr546787/Code_Parser/test/{file_name}.py\n'
    slurm_script += 'sacct -j $SLURM_JOB_ID --format=JobID,Start,End,Elapsed > ${SLURM_JOB_ID}_job_times.log'
    with open(f'test/{file_name}.sh', 'w') as f:
        f.write(slurm_script)


job_index = 0
slurm_script_for_all = ''
def func(list_for_dependency, tree, file_name='0', dependency='', count=0):
    generate_slurm_script(file_name)
    global job_index
    global slurm_script_for_all
    for ele in list_for_dependency:
        if ele['file_name'] == file_name:
            isInForLoop = False
            variable = ''
            values = []
            for loop in loops:
                if ele['lineno'] >= loop.lineno and ele['lineno'] <= loop.end_lineno:
                    isInForLoop = True
                    variable = loop.variable
                    values = loop.values
                    break
            if (not isInForLoop) and dependency == '':
                slurm_script_for_all += f'JOB_ID_{job_index}=$(sbatch --nodes=1 --ntasks=1 --parsable {file_name}.sh {sign} NoDependecy {job_index})\n'
                if file_name in list(tree.keys()):
                    dependency += 'JOB_ID_' + str(job_index)
                    for child in tree[file_name]:
                        ############################
                        job_index += 1
                        func(list_for_dependency, tree,child, dependency)
            elif (not isInForLoop) and dependency != '':
                slurm_script_for_all += f'JOB_ID_{job_index}=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:${dependency} {file_name}.sh {sign} {extract_numbers(dependency)} {job_index})\n'
                if file_name in list(tree.keys()):
                    dependency += ',$JOB_ID_' + str(job_index)
                    for child in tree[file_name]:
                        job_index += 1
                        func(list_for_dependency, tree, child, dependency)
            elif isInForLoop and dependency == '':
                if variable in ele['dependences']:
                    while(count <= len(values) - 1):
                        slurm_script_for_all += f'JOB_ID_{job_index}=$(sbatch --nodes=1 --ntasks=1 --parsable {file_name}.sh {sign} {extract_numbers(dependency)} {job_index} {values[count]})\n'
                        count += 1
                        if file_name in list(tree.keys()):
                            dependency += ',$JOB_ID_' + str(job_index)
                            for child in tree[file_name]:
                                job_index += 1
                                func(list_for_dependency, tree, child, dependency)
                        job_index += 1
                        
                else:
                    while(count <= len(values) - 1):
                        slurm_script_for_all += f'JOB_ID_{job_index}=$(sbatch --nodes=1 --ntasks=1 --parsable {file_name}.sh {sign} {extract_numbers(dependency)} {job_index})\n'
                        count += 1
                        if file_name in list(tree.keys()):
                            dependency += ',$JOB_ID_' + str(job_index)
                            for child in tree[file_name]:
                                job_index += 1
                                func(list_for_dependency, tree, child, dependency)
                        job_index += 1
            # If in the forloop and the dependency not null
            elif isInForLoop and dependency != '':
                if variable in ele['dependences']:
                    while(count <= len(values) - 1):
                        slurm_script_for_all += f'JOB_ID_{job_index}=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:${dependency} {file_name}.sh {sign} {extract_numbers(dependency)} {job_index} {values[count]})\n'
                        count += 1
                        if file_name in list(tree.keys()):
                            temp =dependency + ',$JOB_ID_' + str(job_index)
                            job_index += 1
                            for child in tree[file_name]:
                                func(list_for_dependency, tree, child, temp)
                        else:
                            job_index += 1
                    job_index -= 1
                else:
                    slurm_script_for_all += f'JOB_ID_{job_index}=$(sbatch --nodes=1 --ntasks=1 --parsable --dependency=afterok:${dependency} {file_name}.sh {sign} {extract_numbers(dependency)} {job_index})\n'
                    if file_name in list(tree.keys()):
                        dependency += ',$JOB_ID_' + str(job_index)
                        job_index += 1
                        for child in tree[file_name]:
                            func(list_for_dependency, tree, child, dependency)
                    else:
                        job_index += 1
            break
        
                
# check if node is in forloop
def check_child_node_type(child):
    for parent in forloop_nodes:
        for node in ast.iter_child_nodes(parent):
            if node == child:
                return parent.target.id
    return ""

class ExtractVariables(ast.NodeVisitor):
    def __init__(self):
        self.variables = set()
        self.assignment_targets = set()
        
    def visit_If(self, node):
        self.visit(node.test)
        self.generic_visit(node)

    def visit_While(self, node):
        self.visit(node.test)
        # print(ast.dump(node.test.left.id))
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            # check if it is function
            if (isinstance(node.parent, ast.Call) and node.parent.func == node):
                return
            if node.id not in self.assignment_targets:
                self.variables.add(node.id)

    def visit_Assign(self, node):
        # visit right side of assign node
        self.visit(node.value)
        # record targets
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.assignment_targets.add(target.id)

    def visit_AugAssign(self, node):
        # visit right side of assign node
        self.visit(node.value)
        # record targets
        if isinstance(node.target, ast.Name):
            self.assignment_targets.add(node.target.id)


def extract_variables_from_code(tree):
    # add attribute parent
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node

    extractor = ExtractVariables()
    # visit all if or while nodes
    orelse_variables = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.If, ast.While)):
            extractor.variables |= extract_ids_from_nodes(node.test)
            # print(ast.dump(node.test))
            if node.orelse:
                orelse_extractor = ExtractVariables()
                # read all targets in else block
                for subnode in node.orelse:
                    orelse_extractor.visit(subnode)
                orelse_variables = orelse_extractor.assignment_targets
            for subnode in node.body: 
                extractor.visit(subnode)
    return extractor.variables, extractor.assignment_targets, orelse_variables

class IDCollector(ast.NodeVisitor):
    def __init__(self):
        self.ids = set()

    def visit_Name(self, node):
        self.ids.add(node.id)
        self.generic_visit(node)

def extract_ids_from_nodes(node):
    collector = IDCollector()
    collector.visit(node)
    
    return collector.ids

# need improve
def parse_if_and_while(node):
    condition_vars, assign_targets, orelse_targets = extract_variables_from_code(node)
    if isinstance(node, ast.If):
        process_node(node, assign_targets, orelse_targets)
        new_node = ast.fix_missing_locations(node)
    pass

def add_print_to_block(block, name):
    assign_node = ast.Assign(
        targets=[
            ast.Name(id='job_index', ctx=ast.Store())
        ],
        value=ast.Call(
            func=ast.Name(id='int', ctx=ast.Load()),
            args=[
                ast.Subscript(
                    value=ast.Attribute(
                        value=ast.Name(id='sys', ctx=ast.Load()),
                        attr='argv',
                        ctx=ast.Load()
                    ),
                    slice=ast.Constant(value=3),
                    ctx=ast.Load()
                )
            ],
            keywords=[]
        )
    )
    block.append(assign_node)  # add this assign_node to the end of code block
    # create a new with_node
    with_node = ast.With(
        items=[
            ast.withitem(
                context_expr=ast.Call(
                    func=ast.Name(id='open', ctx=ast.Load()),
                    args=[
                        ast.JoinedStr(
                            values=[
                                ast.Str(s=f'pkl/{name}_{sign}_'),
                                ast.FormattedValue(
                                    value=ast.Name(id='job_index', ctx=ast.Load()),
                                    conversion=-1,
                                    format_spec=None
                                ),
                                ast.Str(s='.pkl')
                            ]
                        ),
                        ast.Str(s='wb')
                    ],
                    keywords=[]
                ),
                optional_vars=ast.Name(id='f', ctx=ast.Store())
            )
        ],
        body=[
            ast.Expr(
                value=ast.Call(
                    func=ast.Attribute(value=ast.Name(id='pickle', ctx=ast.Load()), attr='dump', ctx=ast.Load()),
                    args=[
                        ast.Name(id=f'{name}', ctx=ast.Load()),
                        ast.Name(id='f', ctx=ast.Load())
                    ],
                    keywords=[]
                )
            )
        ]
    )
    block.append(with_node)  # add this with_node to the end of code block

def process_node(node, if_targets, else_targets):
    new_node = copy.deepcopy(node)
    if isinstance(new_node, ast.If):
        for target in if_targets:
            add_print_to_block(new_node.body, target)  # add with node
        if new_node.orelse:
            # we can improve this part later for multiple if or while!!!
            if isinstance(new_node.orelse[0], ast.If):
                process_node(new_node.orelse[0])
            else:
                for else_target in else_targets:
                    add_print_to_block(new_node.orelse, else_target)  # add with node to else block
    if isinstance(new_node, ast.While):
        new_node = ast.unparse(ast.Module(body=[new_node], type_ignores=[]))
        new_node = ast.parse(new_node)
        for target in if_targets:
            add_print_to_block(new_node.body, target)
        return new_node
    # for child in ast.iter_child_nodes(new_node):
    return new_node

if __name__ == "__main__":
    file_path = "test/main.py"
    parse_code(file_path)
    generate_scripts(assign_nodes)
    header = f'''#!/bin/bash

#SBATCH --nodes={job_index + 1}
#SBATCH --ntasks-per-node=1
'''
    with open('test/sbatchfactory.sh', 'w') as f:
        f.write(header + slurm_script_for_all) 
