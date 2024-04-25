import ast

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



# 使用示例
source_code = """
import os
import sys
from datetime import datetime

x = x + 5
print(x) if x > 3 else None
y = 3
if x > 3:
    print("x is greater than 3")
while x < 10:
    a = y
    x += 1
for i in range(x):
    print(i)
"""

import_list, control_flow_list = extract_nodes(source_code)
print("Import Nodes:")
print(import_list)
print("Control Flow Nodes:")
print(control_flow_list)
print(len(control_flow_list))
for node in control_flow_list:
    print(node)
    
