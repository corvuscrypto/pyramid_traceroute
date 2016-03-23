import ast
import sys

class Walker(ast.NodeVisitor):
    def __init__(self):
        self.ctx = ''
        self.aliases = {}
        self.functions = []
        super(Walker, self).__init__()

    def grab_definitions(self, node, ctx):
        for n in ast.iter_child_nodes(node):
            if isinstance(n, ast.FunctionDef):
                if ctx:
                    self.functions.append(ctx+'.'+n.name)
                else:
                    self.functions.append(n.name)

                self.grab_definitions(n, n.name)

    def walk_file(self, f):
        self.ctx = f
        self.aliases = {}
        self.functions = []
        with open(f) as fil:
            node = ast.parse(fil.read())
            self.grab_definitions(node,'')
            self.visit(node)

    def visit_Import(self, node):
        for name in node.__dict__['names']:
            if name.asname:
                self.functions.append(name.asname)
                self.aliases[name.asname] = name.name
            else:
                self.functions.append(name.name)
            ast.NodeVisitor.generic_visit(self, node)

    def visit_Call(self, node):
        func = node.func
        name = self.get_alias(func)
        if name:
            for i in range(len(name.split('.'))):
                s = name.split('.')
                cap = len(s)-i
                if '.'.join(s[:cap]) in self.functions:
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

def test():
    pass

if __name__ == "__main__":
    bool(test())
    walker = Walker()
    walker.walk_file(sys.argv[1])
