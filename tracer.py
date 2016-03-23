import ast
import sys
import os as o

aliases = {}

def deco(func):
    def wrapper():
        print "ho"
    return wrapper

class Walker(ast.NodeVisitor):
    def visit_Import(self, node):
        for name in node.__dict__['names']:
            if name.asname:
                aliases[name.asname] = name.name
            else:
                aliases[name.name] = name.name
            ast.NodeVisitor.generic_visit(self, node)
    def visit_ImportFrom(self, node):
        for name in node.__dict__['names']:
            print name.__dict__
        ast.NodeVisitor.generic_visit(self, node)
    def visit_Call(self, node):
        func = node.func
        name = self.get_alias(func)
        print name
        ast.NodeVisitor.generic_visit(self, node)
    def generic_visit(self, node):
        ast.NodeVisitor.generic_visit(self, node)

    def get_alias(self, node, postfix=''):
        if isinstance(node, ast.Name):
            name = node.id
            name = aliases.get(name,name)
            if postfix:
                name+='.'+postfix
            return name
        elif isinstance(node, ast.Attribute):
            return self.get_alias(node.value, node.attr)


@deco
def test():
    pass

if __name__ == "__main__":
    o.getcwd()
    _root_node = None
    walker = Walker()
    with open(sys.argv[1],'r') as f:
        _root_node = ast.parse(f.read())

    walker.visit(_root_node)
