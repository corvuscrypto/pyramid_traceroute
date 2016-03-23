import ast
import sys
import os as o

def deco(func):
    def wrapper():
        print "ho"
    return wrapper

class Walker(ast.NodeVisitor):
    def __init__(self):
        self.ctx = ''
        self.aliases = {}
        super(Walker, self).__init__()

    def walk_file(self, f):
        self.ctx = f
        self.aliases = {}
        with open(f) as fil:
            self.visit(ast.parse(fil.read()))

    def visit_Import(self, node):
        for name in node.__dict__['names']:
            if name.asname:
                self.aliases[name.asname] = name.name
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
            name = self.aliases.get(name,name)
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
    walker = Walker()
    walker.walk_file(sys.argv[1])
