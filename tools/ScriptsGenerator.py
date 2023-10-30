import ast

# Import some libraries that i need
import_libaries = "import sys\nimport pickle\n"

function = '''
import re, os
dependency = int(sys.argv[2])
sign=int(sys.argv[1])
def find_file(dependency, filename):
    numbers = re.findall(r'\d+', dependency)
    processed_string = '-'.join(numbers)
    indices = (processed_string.split('-'))[::-1]
    for index in indices:
        full_path = os.path.join("/home/hr546787/Code_Parser/pkl/", filename + "_" + str(sign) + "_" + str(index) + ".pkl")
        if os.path.exists(full_path):
            return index
'''

def unparse_code(nodes):
    return ast.unparse(ast.Module(body=nodes, type_ignores=[]))

def generate_pickle_code_for_input(assign_nodes, variable, sign):
    generated_code = []
    generated_code.append(function)
    variables = []
    for node in assign_nodes:
        if isinstance(node.value, ast.Call):
            for arg in node.value.args:
                if isinstance(arg, ast.Name):
                    if arg.id != variable:
                        variables.append(arg.id)
                    else:
                        generated_code.append(f"\n{variable}=float(sys.argv[4])\n")
                        
            for keyword in node.value.keywords:
                if isinstance(keyword, ast.keyword):
                    if keyword.arg != variable:
                        variables.append(keyword.arg)
                    else:
                        generated_code.append(f"\n{variable}=float(sys.argv[4])\n")
        elif isinstance(node.value, ast.Name):
            if node.value.id != variable:
                variables.append(node.value.id)
            else:
                generated_code.append(f"\n{variable}=float(sys.argv[4])\n")
                          
    variables = list(set(variables))
    for var in variables:
        generated_code.append(f"\nindex=find_file(dependency, '{var}')\nwith open(f'/home/hr546787/Code_Parser/pkl/{var}_{sign}_{{index}}.pkl', 'rb') as f:\n    {var} = pickle.load(f)\n")
    return generated_code

def generate_pickle_code_for_ouput(assign_nodes, sign):
    generated_code = []
    for node in assign_nodes:
        generated_code.append(f"\njob_index=int(sys.argv[3])")
        for target in node.targets:
            if isinstance(target, ast.Name):
                target_name = target.id
                generated_code.append(
                    f"\nwith open(f'/home/hr546787/Code_Parser/pkl/{target_name}_{sign}_{{job_index}}.pkl', 'wb') as f:\n    pickle.dump({target_name}, f)\n"
                )
            elif isinstance(target, ast.Tuple):
                for elt in target.elts:
                    if isinstance(elt, ast.Name):
                        target_name = elt.id
                        generated_code.append(
                            f"\nwith open(f'/home/hr546787/Code_Parser/pkl/{target_name}_{sign}_{{job_index}}.pkl', 'wb') as f:\n    pickle.dump({target_name}, f)\n"
                        )
    return generated_code

def generate_python_script(import_nodes , nodes, name, sign, variable=None, pos=''):
    code = ''
    if pos == 'start':
        code = unparse_code(import_nodes + nodes)
        code += '\n'.join(generate_pickle_code_for_ouput(nodes, sign))
    else:
        code = unparse_code(import_nodes)+ '\n'.join(generate_pickle_code_for_input(nodes,variable, sign)) + '\n'+ unparse_code(nodes)
        if pos != 'end':
            code += '\n'.join(generate_pickle_code_for_ouput(nodes, sign))
    with open("test/" + name + ".py", "w") as f:
        f.write(import_libaries + code)
        
def generate_input_code(variables, sign):
    generated_code = []
    generated_code.append(function)
    for var in variables:
        generated_code.append(f"\nindex=find_file(dependency,'{var}')\nwith open(f'/home/hr546787/Code_Parser/pkl/{var}_{sign}_{{index}}.pkl', 'rb') as f:\n    {var} = pickle.load(f)\n")
    return generated_code