import ast
from models import IfStmt

def walk(node):
    for n in ast.iter_child_nodes(node):
        parse_node(n)
        walk(n)

def parse_node(node):
    if isinstance(node, ast.If):
        print IfStmt(node).clause
    elif isinstance(node, ast.For) or isinstance(node, ast.While):
        print "loop"
    elif isinstance(node, ast.Call):
        print "call"

if __name__ == "__main__":
    with open("./test_file.py") as test:
        main_node = ast.parse(test.read())
        walk(main_node)
