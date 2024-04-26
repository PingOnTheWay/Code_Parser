import ast
from collections import defaultdict
import random
import os
import astor

sign = random.randint(10000, 1000000)

def extract_nodes(source_code):
    tree = ast.parse(source_code)
    import_nodes = []
    control_flow_nodes = []

    def traverse(node):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            import_nodes.append(node)
        elif isinstance(node, (ast.Assign, ast.While, ast.If, ast.For)):
            control_flow_nodes.append(node)
            # For while, if, and for nodes, we do not traverse child nodes
            return
        elif isinstance(node, ast.Call):
            control_flow_nodes.append(node)
        # Traverse all child nodes of the current node
        for child in ast.iter_child_nodes(node):
            traverse(child)

    traverse(tree)  # Start traversal from the root node of the tree

    return import_nodes, control_flow_nodes

def read_and_process_code(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with open(file_path, 'r') as file:
        source_code = file.read()

    return source_code

# Example usage
source_code = read_and_process_code("test/main.py")

import_list, control_flow_list = extract_nodes(source_code)

class ExtractVariables(ast.NodeVisitor):
    def __init__(self):
        self.variables = set()
        self.assignment_targets = set()
        
    def visit_If(self, node):
        self.visit(node.test)
        self.generic_visit(node)

    def visit_While(self, node):
        self.visit(node.test)
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            # Check if it is a function
            if ((isinstance(node.parent, ast.Call) and node.parent.func == node)):
                return
            if node.id not in self.assignment_targets:
                self.variables.add(node.id)

    def visit_Assign(self, node):
        # Visit the right side of the assign node
        self.visit(node.value)
        # Record targets
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.assignment_targets.add(target.id)

    def visit_AugAssign(self, node):
        # Visit the right side of the assign node
        self.visit(node.value)
        # Record targets
        if isinstance(node.target, ast.Name):
            self.assignment_targets.add(node.target.id)
            
class IDCollector(ast.NodeVisitor):
    def __init__(self):
        self.ids = set()

    def visit_Name(self, node):
        if not self._is_attribute_value(node) or isinstance(node.ctx, ast.Load):
            self.ids.add(node.id)
        self.generic_visit(node)
    
    def visit_Call(self, node):
        # handle args
        for arg in node.args:
            self.visit(arg)
        # handle keywords
        for keyword in node.keywords:
            self.visit(keyword.value)
        # jump over func id
        self.generic_visit(node.func)
    
    def _is_attribute_value(self, node):
        # 检查这个节点是否是某个 ast.Attribute 的 value
        parent = getattr(node, 'parent', None)
        return isinstance(parent, ast.Attribute) and parent.value is node
    
        
def extract_ids_from_nodes(node):
    collector = IDCollector()
    collector.visit(node)
    
    return collector.ids

def extract_variables_from_code(tree):
    # Add attribute parent
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node

    extractor = ExtractVariables()
    # Visit all if or while nodes
    orelse_variables = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.If, ast.While)):
            extractor.variables |= extract_ids_from_nodes(node.test)
            if node.orelse:
                orelse_extractor = ExtractVariables()
                # Read all targets in else block
                for subnode in node.orelse:
                    orelse_extractor.visit(subnode)
                orelse_variables = orelse_extractor.assignment_targets
            for subnode in node.body: 
                extractor.visit(subnode)
    return extractor.variables, extractor.assignment_targets, orelse_variables

# Create a visitor class to collect all ids on the left side of assignments
class AssignmentCollector(ast.NodeVisitor):
    def __init__(self):
        self.ids = set()

    def visit_Assign(self, node):
        # Traverse all targets and extract ids
        for target in node.targets:
            self.handle_target(target)
        self.generic_visit(node)

    def handle_target(self, target):
        # Handle Name node
        if isinstance(target, ast.Name):
            self.ids.add(target.id)
        # Handle complex targets like tuples or lists
        elif isinstance(target, (ast.Tuple, ast.List)):
            for elt in target.elts:
                self.handle_target(elt)
        # Handle subscript used for dictionary keys or list indexing
        elif isinstance(target, ast.Subscript):
            if isinstance(target.value, ast.Name):
                self.ids.add(target.value.id)  # Collect the variable name of the subscript

def parse_assign_node(assign_node, index):
    is_for = False
    # Parse targets
    if isinstance(assign_node, (ast.While, ast.If)):
        # print("While or If")
        # print(ast.dump(assign_node))
        dependences, if_vars, orelse_vars = extract_variables_from_code(assign_node)
        dependences = list(dependences)
        collector = AssignmentCollector()
        collector.visit(assign_node)
        # print(dependences)
        if_vars |= orelse_vars
        collector.ids |= if_vars
        targets = list(collector.ids)
    elif isinstance(assign_node, ast.Call):
        dependences = [arg.id for arg in assign_node.args if isinstance(arg, ast.Name)]
        dependences += [keyword.value.id if isinstance(keyword.value, ast.Name) else keyword.value.value for keyword in assign_node.keywords]
        targets = []
    elif isinstance(assign_node, ast.For):
        iter_node = assign_node.iter
        if isinstance(iter_node, ast.List):
            values = [const.value for const in iter_node.elts if isinstance(const, ast.Constant)]
        # print(values)
        # print(ast.dump(assign_node.target))
        # print(assign_node.target.id)
        is_for = True
        targets = []
        dependences = []
        for child in assign_node.body:
            # print("Child")
            # print(ast.dump(child))
            targets += parse_assign_node(child, index)["targets"]
            dependences += parse_assign_node(child, index)["dependences"]
            # print(dependences)
            # print("")
        dependences = [x for x in dependences if x != assign_node.target.id]
    elif isinstance(assign_node, ast.Expr):
        # print(ast.dump(assign_node))
        # print("Expr")
        targets = []
        dependences = []
        targets += parse_assign_node(assign_node.value, index)["targets"]
        dependences += parse_assign_node(assign_node.value, index)["dependences"]
    else:
        # print("Assign")
        # print(ast.dump(assign_node))
        targets=[]
        for target in assign_node.targets:
            if isinstance(target, ast.Name):
                targets.append(target.id)
            elif isinstance(target, ast.Tuple):
                for elt in target.elts:
                    if isinstance(elt, ast.Name):
                        targets.append(elt.id)
        dependences = []
        
        if isinstance(assign_node.value, ast.Call):
            dependences = [arg.id for arg in assign_node.value.args if isinstance(arg, ast.Name)]
            dependences += [keyword.value.id for keyword in assign_node.value.keywords if isinstance(keyword.value, ast.Name)]
        elif isinstance(assign_node.value, ast.Name):
            dependences.append(assign_node.value.id) 
        else:
            collector = IDCollector()
            collector.visit(assign_node.value)
            dependences = collector.ids
    return {
        'targets': list(set(targets)),
        'dependences': list(set([item for item in dependences if not isinstance(item, (int, float))])),
        'lineno': assign_node.lineno,
        'file_name': index,
        'node': index,
        'for' : is_for,
        'iter': values if is_for else None,
        'iter_var': assign_node.target.id if is_for else None
    }

def flatten_list(nested_list):
    flat_list = []
    # Recursive function to flatten a list
    def flatten(item):
        if isinstance(item, list):
            for sub_item in item:
                flatten(sub_item)
        else:
            flat_list.append(item)

    # Start flattening the passed list
    flatten(nested_list)
    return flat_list

def process_dependencies(dependencies):
    i = len(dependencies) - 1
    while i > 0:
        current = dependencies[i]
        previous = dependencies[i - 1]

        # Step 1: Skip if the current or previous item's 'for' is not False
        if current.get('for') or previous.get('for'):
            i -= 1
            continue

        # Step 3: Check if any dependence of current is in targets of previous
        if any(dep in previous['targets'] for dep in current['dependences']):
            # Add targets and dependences of current to previous, remove duplicates
            previous['targets'] = list(set(previous['targets'] + current['targets']))
            previous['dependences'] = list(set(previous['dependences'] + current['dependences']))

            # Merge file_name info
            if not isinstance(previous['node'], list):
                previous['node'] = [previous['node']]
            previous['node'].append(current['node'])
            previous['node'] = flatten_list(previous['node'])

            # Remove the current element
            dependencies.pop(i)
        
        i -= 1

    return dependencies

def refine_dependencies(dependency_list):
    # Create a set to store all previously encountered targets
    all_previous_targets = set()

    # Traverse each element
    for entry in dependency_list:
        # Add the current element's targets to the global set
        current_targets = set(entry['targets'])
        
        # Check the current element's dependences
        filtered_dependencies = [
            dep for dep in entry['dependences']
            if dep in all_previous_targets  # Only keep dependences that have been encountered before
        ]
        
        # Update the current element's dependences
        entry['dependences'] = filtered_dependencies
        
        # Update the set of previously encountered targets
        all_previous_targets.update(current_targets)

    return dependency_list
    
def build_dependency_map(nodes):
    # Initialize a tree as a defaultdict
    list_for_dependency = []
    for index, node in enumerate(nodes):
        list_for_dependency.append(parse_assign_node(node, index))
    # Process the dependency list
    print("Processed List")
    length = len(list_for_dependency)
    processed_list = process_dependencies(list_for_dependency)
    while length != len(processed_list):
        length = len(processed_list)
        processed_list = process_dependencies(processed_list)
    processed_list = refine_dependencies(processed_list)
    dependency_map = {i: [] for i in range(len(processed_list))}

    # Traverse each element in the list, record its index and content
    for i, current in enumerate(processed_list):
        current_deps = current['dependences']
        # If the current element has dependencies, check if these dependencies appear in any earlier element's targets
        if current_deps:
            # Traverse all elements before the current index
            for j in range(i):
                previous_targets = processed_list[j]['targets']
                # Check each dependency of the current element to see if it is found in any earlier element's targets
                for dep in current_deps:
                    if dep in previous_targets:
                        # If a dependency is found in an earlier element's targets, add that element's index to the dependency map
                        dependency_map[i].append(j)
    return  processed_list, dependency_map

def generate_trigger_slurm_script(dependency_list, dependency_map):
    script_lines = ["#!/bin/bash", "\n#SBATCH --ntasks-per-node=1"]
    job_ids = []
    job_map = defaultdict(list)
    fix = 0

    for index, item in enumerate(dependency_list):
        base_command = f"sbatch --nodes=1 --ntasks=1 --parsable"
        job_var = f"JOB_ID"
        dependencies = dependency_map.get(index, [])

        # Check if this is a 'for' loop with iterables
        if item.get('for') and item.get('iter'):
            # Handle for loop by creating multiple jobs
            for i, iter_val in enumerate(item['iter']):
                dep_jobs = []
                if dependencies:
                    job_map[index].append(index + fix)
                    dep_jobs = [job_ids[d] for d in dependencies]  
                    for d in dependencies:
                        if d in job_map:
                            dep_jobs.extend(job_map[d])
                            dep_jobs = list(set(dep_jobs))
                dep_str = f"--dependency=afterok:{','.join(f'$JOB_ID_{d}' for d in dep_jobs)}" if dep_jobs else ""
                command = f'{job_var}_{index + fix}=$({base_command} {dep_str} /home/hr546787/Code_Parser/test/{index}.sh {sign} {index} {iter_val})'
                fix += 1
                script_lines.append(command)
            fix -= 1
        else:
            # Normal job submission
            dep_jobs = []
            if dependencies:
                job_map[index].append(index + fix)
                dep_jobs = [job_ids[d] for d in dependencies]  
                for d in dependencies:
                    if d in job_map:
                        dep_jobs.extend(job_map[d])
                        dep_jobs = list(set(dep_jobs))
            dep_str = f"--dependency=afterok:{','.join(f'$JOB_ID_{d}' for d in dep_jobs)}" if dep_jobs else ""
            command = f'{job_var}_{index + fix}=$({base_command} {dep_str} /home/hr546787/Code_Parser/test/{index}.sh {sign} NoDependency {index})'
            script_lines.append(command)

        job_ids.append(index + fix)
    script_lines.append(f"sacct -j $SLURM_JOB_ID --format=JobID,Start,End,Elapsed > /home/hr546787/Code_Parser/results/test1/trigger_{sign}_log.log\n")
    return "\n".join(script_lines)

def save_script_to_file(script_content, file_path):
    """ Save the generated script content to a file. """
    with open(file_path, 'w') as file:
        file.write(script_content)

def generate_slurm_scripts(dependency_list, script_dir):
    # Ensure the output directory exists
    os.makedirs(script_dir, exist_ok=True)
    
    for index, item in enumerate(dependency_list):
        filename = f"{index}.sh"
        # Generate a SLURM script for each project, including iterable items
        create_slurm_script(script_dir, filename, item, index)

def create_slurm_script(directory, filename, item, job_index):
    # Build the SLURM script content
    path = os.path.join(directory, filename)
    with open(path, 'w') as file:
        file.write("#!/usr/local_rwth/bin/zsh\n")
        file.write(f"#SBATCH --job-name={job_index}\n")

        # Add Python execution command
        base_command = f"/rwthfs/rz/cluster/home/hr546787/Code_Parser/new_env/bin/python /home/hr546787/Code_Parser/test/{job_index}.py $1 $2 $3"
        
        # If it's a loop structure, add a command line for each iteration value
        command = f"srun {base_command}"
        file.write(f"{command}\n")
        
        # Add SACCT command
        file.write("sacct -j $SLURM_JOB_ID --format=JobID,Start,End,Elapsed > /home/hr546787/Code_Parser/results/test1/${SLURM_JOB_ID}_$1_log.log\n")



processed_list, dependency_map = build_dependency_map(control_flow_list)
print(processed_list)
print(dependency_map)
slurm_script = generate_trigger_slurm_script(processed_list, dependency_map)
save_script_to_file(slurm_script, 'test/trigger_slurm_script.sh')
generate_slurm_scripts(processed_list, "test")

def generate_python_scripts(dependency_list, import_list, control_flow_list, output_dir):
    os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists

    # Basic import statements
    imports = "\n".join(astor.to_source(node) for node in import_list) + "import re, os, pickle, sys\n"

    for index, item in enumerate(dependency_list):
        script_content = imports  # Start each script file's content
        script_content += f"sign = sys.argv[1]\n"

        # Handle dependencies
        if item['dependences'] and dependency_map[index]:
            for dep in item['dependences']:
                script_content += f"with open(f'/home/hr546787/Code_Parser/pkl/{dep}_{{sign}}.pkl', 'rb') as f:\n"
                script_content += f"    {dep} = pickle.load(f)\n\n"

        # Handle loop iteration variable
        if item['for'] and item['iter_var']:
            script_content += f"{item['iter_var']} = float(sys.argv[3])\n"

        # Add control flow code
        node_indices = item['node'] if isinstance(item['node'], list) else [item['node']]
        for node_index in node_indices:
            node = control_flow_list[node_index]
            if isinstance(node, ast.For) and item['for']:
                # Only translate the body part of the for loop
                for body_item in node.body:
                    script_content += astor.to_source(body_item)
            else:
                script_content += astor.to_source(node)

        # Handle targets, if any, save them
        initial_targets = ''
        if item['targets']:
            for target in item['targets']:
                script_content += f"with open(f'/home/hr546787/Code_Parser/pkl/{target}_{{sign}}.pkl', 'wb') as f:\n"
                script_content += f"    pickle.dump({target}, f)\n"
                initial_targets += f"{target} = None\n"

        # Save the generated script to a file
        with open(os.path.join(output_dir, f"{index}.py"), 'w') as file:
            file.write(initial_targets + script_content)
generate_python_scripts(processed_list, import_list, control_flow_list, "test/")
