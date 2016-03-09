import ast
import ast_helpers

class File():
    def __init__(self):
        self.aliases = {}
        pass

class Member():
    def __init__(self, name, route=None):
        # route if any
        self._route = route
        # member aliases {alias: actual.path.to.function}
        # e.g. import module.submodule -> {submodule: module.submodule}
        self.aliases = {}
        # member calls
        self.calls = []

class Call():
    def __init__(self, function=None):
        self._function = function

class Control():
    def __init__(self, _type=None):
        self.calls = []
        self._type = _type

class ControlCall(Call):
    def __init__(self, function=None, clause=""):
        self.clause = clause
        super(self.__class__, self).__init__(function)

class ConditionalSet():
    def __init__(self, node):
        self.conditionals = []
        x = node
        while(isinstance(x, ast.If)):
            ast_helpers.parsed_scope_nodes.append(x)
            self.conditionals.append(IfStmt(x))

            if len(x.orelse)>0 and isinstance(x.orelse[0], ast.If):
                x = x.orelse[0]
            elif x.orelse != []:
                x = x.orelse
            else:
                x = None
        if x is not None:
            self.conditionals.append(ElseStmt(x))
        print [x.clause for x in self.conditionals]

class IfStmt():
    def __init__(self, node):
        self.clause = IfStmt.compile_clause(node)
        self.body = None

    @staticmethod
    def compile_clause(node):
        test = node.test
        if isinstance(test, list):
            pass
        else:
            if isinstance(test, ast.BoolOp):
                return ast_helpers.parse_bool(test)
            elif isinstance(test, ast.Compare):
                return ast_helpers.parse_compare(test)
            else:
                return ast_helpers.node_to_string(test)

class ElseStmt():
    def __init__(self, body):
        self.clause = "else"
        self.body = None
