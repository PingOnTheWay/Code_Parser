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
            # 对于 while, if, for 节点，我们不遍历子节点
            return
        elif isinstance(node, ast.Call):
            control_flow_nodes.append(node)
        # 遍历当前节点的所有子节点
        for child in ast.iter_child_nodes(node):
            traverse(child)

    traverse(tree)  # 从树的根节点开始遍历

    return import_nodes, control_flow_nodes

def read_and_process_code(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with open(file_path, 'r') as file:
        source_code = file.read()

    print("Read source code:")
    print(source_code)

    return source_code

# 使用示例
source_code = read_and_process_code("/Users/pingwan/Desktop/Thesis_Project/Code_Parser/test/main.py")

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

def parse_assign_node(assign_node, index):
    is_for = False
    # Parse targets
    if isinstance(assign_node, (ast.While, ast.If)):
        # print("While or If")
        dependences, if_vars, orelse_vars = extract_variables_from_code(assign_node)
        dependences = list(dependences)
        if_vars |= orelse_vars
        targets = list(if_vars)
    elif isinstance(assign_node, ast.Call):
        # print("Call")
        # print(ast.dump(assign_node))
        dependences = [arg.id for arg in assign_node.args if isinstance(arg, ast.Name)]
        # dependences = [arg.id if isinstance(arg, ast.Name) else arg.value for arg in assign_node.args]
        dependences += [keyword.value.id if isinstance(keyword.value, ast.Name) else keyword.value.value for keyword in assign_node.keywords]
        targets = []
    elif isinstance(assign_node, ast.For):
        # print("For")
        # print(ast.dump(assign_node))
        iter_node = assign_node.iter
        if isinstance(iter_node, ast.List):
            values = [const.value for const in iter_node.elts if isinstance(const, ast.Constant)]
        print(values)
        print(ast.dump(assign_node.target))
        print(assign_node.target.id)
        is_for = True
        targets = []
        dependences = []
        for child in assign_node.body:
            # print(ast.dump(child))
            targets += parse_assign_node(child, index)["targets"]
            dependences += parse_assign_node(child, index)["dependences"]
        dependences = [x for x in dependences if x != assign_node.target.id]
    elif isinstance(assign_node, ast.Expr):
        print(ast.dump(assign_node))
        print("Expr")
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
        # Initialize args and keywords
        dependences = []
        
        # Parse args and keywords if value is a Call node
        if isinstance(assign_node.value, ast.Call):
            dependences = [arg.id for arg in assign_node.value.args if isinstance(arg, ast.Name)]
            # dependences = [arg.id if isinstance(arg, ast.Name) else arg.value for arg in assign_node.value.args]
            dependences += [keyword.value.id if isinstance(keyword.value, ast.Name) else keyword.value.value for keyword in assign_node.value.keywords]
        elif isinstance(assign_node.value, ast.Name):
            dependences.append(assign_node.value.id)    
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
    # 递归函数来展开列表
    def flatten(item):
        if isinstance(item, list):
            for sub_item in item:
                flatten(sub_item)
        else:
            flat_list.append(item)

    # 开始展开传入的列表
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
    # 创建一个集合用来存储所有之前遇到的targets
    all_previous_targets = set()
    
    # 遍历每个元素
    for entry in dependency_list:
        # 当前元素的targets添加到全局集合中
        current_targets = set(entry['targets'])
        
        # 检查当前元素的dependences
        filtered_dependencies = [
            dep for dep in entry['dependences']
            if not (dep in current_targets and dep not in all_previous_targets)
        ]
        
        # 更新当前元素的dependences
        entry['dependences'] = filtered_dependencies
        
        # 更新之前遇到的targets集合
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
    # for item in processed_list:
    #     print(item)
    dependency_map = {i: [] for i in range(len(processed_list))}

    # 遍历列表中的每个元素，记录它的索引和内容
    for i, current in enumerate(processed_list):
        current_deps = current['dependences']
        # 如果当前元素有依赖，检查这些依赖是否出现在前面任一元素的targets中
        if current_deps:
            # 遍历当前索引之前的所有元素
            for j in range(i):
                previous_targets = processed_list[j]['targets']
                # 检查当前元素的每个依赖是否在之前元素的targets中
                for dep in current_deps:
                    if dep in previous_targets:
                        # 如果依赖项在前面某个元素的targets中找到了，添加那个元素的索引到依赖映射中
                        dependency_map[i].append(j)

    return  processed_list, dependency_map

def generate_trigger_slurm_script(dependency_list, dependency_map):
    script_lines = ["#!/bin/bash", "\n#SBATCH --ntasks-per-node=1"]
    job_ids = []
    fix = 0

    for index, item in enumerate(dependency_list):
        base_command = f"sbatch --nodes=1 --ntasks=1 --parsable"
        job_var = f"JOB_ID"
        dependencies = dependency_map.get(index, [])

        # Check if this is a 'for' loop with iterables
        if item.get('for') and item.get('iter'):
            # Handle for loop by creating multiple jobs
            for i, iter_val in enumerate(item['iter']):
                dep_str = f"--dependency=afterok:{','.join(f'$JOB_ID_{d}' for d in dependencies)}" if dependencies else "NoDependency"
                command = f'{job_var}_{index + fix}=$({base_command} {dep_str} {index}.sh {sign} {index} {iter_val})'
                fix += 1
                script_lines.append(command)
        else:
            # Normal job submission
            dep_str = f"--dependency=afterok:{','.join(f'$JOB_ID_{d}' for d in dependencies)}" if dependencies else "NoDependency"
            command = f'{job_var}_{index + fix}=$({base_command} {dep_str} {index}.sh {sign} NoDependency {index})'
            script_lines.append(command)

        job_ids.append(job_var)

    return "\n".join(script_lines)

def save_script_to_file(script_content, file_path):
    """ Save the generated script content to a file. """
    with open(file_path, 'w') as file:
        file.write(script_content)

def generate_slurm_scripts(dependency_list, script_dir):
    # 确保输出目录存在
    os.makedirs(script_dir, exist_ok=True)
    
    for index, item in enumerate(dependency_list):
        filename = f"{index}.sh"
        # 为每个项目生成一个 SLURM 脚本，包括迭代项目
        create_slurm_script(script_dir, filename, item, index)

def create_slurm_script(directory, filename, item, job_index):
    # 构建 SLURM 脚本内容
    path = os.path.join(directory, filename)
    with open(path, 'w') as file:
        file.write("#!/usr/local_rwth/bin/zsh\n")
        file.write(f"#SBATCH --job-name={job_index}\n")
        file.write("#SBATCH --output=/dev/null\n\n")

        # 添加 Python 执行命令
        base_command = f"/rwthfs/rz/cluster/home/hr546787/Code_Parser/new_env/bin/python /home/hr546787/Code_Parser/test/{job_index}.py $1 $2 $3"
        
        # # 如果是循环结构，为每个迭代值添加一个命令行
        # if item.get('for') and item.get('iter'):
        #     for iter_value in item['iter']:
        #         command = f"srun {base_command} {iter_value}"
        #         file.write(f"{command}\n")
        # else:
        command = f"srun {base_command}"
        file.write(f"{command}\n")
        
        # 添加 SACCT 命令
        file.write("sacct -j $SLURM_JOB_ID --format=JobID,Start,End,Elapsed > ${SLURM_JOB_ID}_${job_index}_log.log\n")



processed_list, dependency_map = build_dependency_map(control_flow_list)
print(processed_list)
print(dependency_map)
# print(import_list)
# print(control_flow_list)
slurm_script = generate_trigger_slurm_script(processed_list, dependency_map)
save_script_to_file(slurm_script, 'test/trigger_slurm_script.sh')
generate_slurm_scripts(processed_list, "/Users/pingwan/Desktop/Thesis_Project/Code_Parser/test")

def generate_python_scripts(dependency_list, import_list, control_flow_list, output_dir):
    os.makedirs(output_dir, exist_ok=True)  # 确保输出目录存在

    # 基本的导入语句
    imports = "\n".join(astor.to_source(node) for node in import_list) + "import re, os, pickle, sys\n"

    for index, item in enumerate(dependency_list):
        script_content = imports  # 开始每个脚本文件的内容
        script_content += f"sign = sys.argv[1]\n"

        # 处理依赖
        if item['dependences'] and dependency_map[index]:
            for dep in item['dependences']:
                script_content += f"with open(f'/home/hr546787/Code_Parser/pkl/{dep}_{{sign}}.pkl', 'rb') as f:\n"
                script_content += f"    {dep} = pickle.load(f)\n\n"

        # 处理循环迭代变量
        if item['for'] and item['iter_var']:
            script_content += f"{item['iter_var']} = float(sys.argv[3])\n"

        # 添加 control flow 中的代码
        node_indices = item['node'] if isinstance(item['node'], list) else [item['node']]
        for node_index in node_indices:
            node = control_flow_list[node_index]
            if isinstance(node, ast.For) and item['for']:
                # 只翻译 for 循环的 body 部分
                for body_item in node.body:
                    script_content += astor.to_source(body_item)
            else:
                script_content += astor.to_source(node)

        # 处理targets，如果有的话，保存它们
        if item['targets']:
            for target in item['targets']:
                script_content += f"with open(f'/home/hr546787/Code_Parser/pkl/{target}_{{sign}}.pkl', 'wb') as f:\n"
                script_content += f"    pickle.dump({target}, f)\n"

        # 保存生成的脚本到文件
        with open(os.path.join(output_dir, f"{index}.py"), 'w') as file:
            file.write(script_content)
generate_python_scripts(processed_list, import_list, control_flow_list, "test/")