import ast
from models import ConditionalSet
from ast_helpers import parsed_scope_nodes

def walk(node):
    for n in ast.iter_child_nodes(node):
        parse_node(n, node)
        walk(n)

def parse_node(node, parent):
    if isinstance(node, ast.If) and node not in parsed_scope_nodes:
        c =ConditionalSet(node)
    elif isinstance(node, ast.For) or isinstance(node, ast.While):
        print "loop"
    elif isinstance(node, ast.Call):
        pass
if __name__ == "__main__":
    with open("./test_file.py") as test:
        main_node = ast.parse(test.read())
        walk(main_node)
