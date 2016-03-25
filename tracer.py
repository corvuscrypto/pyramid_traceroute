import ast
import sys

class Walker(ast.NodeVisitor):
    def __init__(self):
        self.ctx = ''
        self.aliases = {}
        self.functions = []
        super(Walker, self).__init__()

    def grab_local_definitions(self, node, ctx=''):
        for n in ast.iter_child_nodes(node):
            if isinstance(n, ast.FunctionDef) or isinstance(n,ast.ClassDef):
                temp_ctx = ctx+n.name
                if not ctx:
                    self.functions.append(n.name)
                else:
                    self.functions.append(temp_ctx)
                subfuncs = self.grab_local_definitions(n, temp_ctx+'.')
        return ''

    def grab_external_import_aliases(self, node):
        for n in ast.iter_child_nodes(node):
            self.grab_external_import_aliases(n)
            if isinstance(n, ast.Import):
                for x in n.names:
                    name = x.name
                    asname = x.asname
                    if asname is None:
                        asname = name
                    self.aliases[asname]=name
            elif isinstance(n, ast.ImportFrom):
                module = n.module
                for x in n.names:
                    name = x.name
                    asname = x.asname
                    if asname is None:
                        asname = name
                    self.aliases[asname]=module+'.'+name

    def walk_routes(self,node):
        pass

    def walk_file(self, f):
        self.ctx = f
        self.aliases = {}
        self.functions = []
        with open(f) as fil:
            node = ast.parse(fil.read())
            self.grab_local_definitions(node)
            self.grab_external_import_aliases(node)
            self.visit(node)

    def generic_visit(self, node):
        try:
            for decorator in node.decorator_list:
                for keyword in decorator.keywords:
                    if keyword.arg == "route_name":
                        print keyword.value.s
        except:
            pass
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
def test_deco(f):
    def func():
        f()
    return func

@test_deco
def test():
    def test2():
        pass
    test2()
    pass

if __name__ == "__main__":
    bool(test())
    walker = Walker()
    walker.walk_file(sys.argv[1])
