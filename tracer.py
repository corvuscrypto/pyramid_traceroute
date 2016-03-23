import ast
import sys

class Walker(ast.NodeVisitor):
    def visit_Module(self, node):
        self.generic_visit(node)
    def visit_If(self, node):
        print "IF"
        ast.NodeVisitor.generic_visit(self, node)
    def generic_visit(self, node):
        print node
        ast.NodeVisitor.generic_visit(self, node)

if __name__ == "__main__":
    _root_node = None
    walker = Walker()
    with open(sys.argv[1],'r') as f:
        _root_node = ast.parse(f.read())

    walker.visit(_root_node)
