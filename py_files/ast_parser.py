import ast
import sys
import os


def walk_functions(scope,depth,stack):
    for func in ast.iter_child_nodes(scope):
        if isinstance(func, ast.FunctionDef):
            stack.append((depth, func.name))
        if isinstance(func, ast.ClassDef):
            stack.append((depth, "__CLASS__."+func.name))
        walk_functions(func,depth+1,stack)
    return stack

def parse_ast(file):
    with open(file, "rt") as data:
        return ast.parse(data.read(), filename=file)


def get_project_files(folder):
    pythonfiles = []
    for (dirpath, dirnames, filenames) in os.walk(folder):
        for f in filenames:
            if os.path.splitext(dirpath+f)[1] == '.py':
                pythonfiles.append(os.path.join(dirpath[len(folder):],f))
    return pythonfiles

def parse_file(dirname, filename):
    tree = parse_ast(os.path.join(dirname, filename))
    stack = [(0,filename)]
    for line in walk_functions(tree, 1, stack):
        print "{},{}".format(line[0],line[1])

if __name__ == "__main__":
    for dirname in sys.argv[1:]:
        print "{},{}".format(-1,dirname)
        for f in get_project_files(dirname):
            parse_file(dirname, f)
