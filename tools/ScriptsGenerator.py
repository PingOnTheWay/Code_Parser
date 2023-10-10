import ast

# Import some libraries that i need
import_libaries = "import sys\nimport pickle\n"

def unparse_code(nodes):
    return ast.unparse(ast.Module(body=nodes, type_ignores=[]))

def generate_pickle_code_for_input(assign_nodes, variable):
    generated_code = []
    variables = []
    for node in assign_nodes:
        if isinstance(node.value, ast.Call):
            for arg in node.value.args:
                if isinstance(arg, ast.Name):
                    if arg.id != variable:
                        variables.append(arg.id)
                    else:
                        generated_code.append(f"\n{variable}=float(sys.argv[1])\n")
                        
            for keyword in node.value.keywords:
                if isinstance(keyword, ast.keyword):
                    if keyword.arg != variable:
                        variables.append(keyword.arg)
                    else:
                        generated_code.append(f"\n{variable}=float(sys.argv[1])\n")
        elif isinstance(node.value, ast.Name):
            if node.value.id != variable:
                variables.append(node.value.id)
            else:
                generated_code.append(f"\n{variable}=float(sys.argv[1])\n")
                          
    variables = list(set(variables))
    for var in variables:
        generated_code.append(f"\nwith open('pkl/{var}.pkl', 'rb') as f:\n    {var} = pickle.load(f)\n")
    return generated_code

def generate_pickle_code_for_ouput(assign_nodes):
    generated_code = []
    for node in assign_nodes:
        for target in node.targets:
            if isinstance(target, ast.Name):
                target_name = target.id
                generated_code.append(
                    f"\nwith open('pkl/{target_name}.pkl', 'wb') as f:\n    pickle.dump({target_name}, f)\n"
                )
            elif isinstance(target, ast.Tuple):
                for elt in target.elts:
                    if isinstance(elt, ast.Name):
                        target_name = elt.id
                        generated_code.append(
                            f"\nwith open('pkl/{target_name}.pkl', 'wb') as f:\n    pickle.dump({target_name}, f)\n"
                        )
    return generated_code

def generate_python_script(import_nodes , nodes, name, variable=None, pos=''):
    code = ''
    if pos == 'start':
        code = unparse_code(import_nodes + nodes)
        code += '\n'.join(generate_pickle_code_for_ouput(nodes))
    else:
        code = unparse_code(import_nodes)+ '\n'.join(generate_pickle_code_for_input(nodes,variable)) + '\n'+ unparse_code(nodes)
        if pos != 'end':
            code += '\n'.join(generate_pickle_code_for_ouput(nodes))
    with open("test/" + name + ".py", "w") as f:
        f.write(import_libaries + code)
        
def generate_input_code(variables):
    generated_code = []
    for var in variables:
        generated_code.append(f"\nwith open('pkl/{var}.pkl', 'rb') as f:\n    {var} = pickle.load(f)\n")
    return generated_code