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

class IfStmt():
    def __init__(self, node):
        self.clause = IfStmt.compile_clause(node)

    @staticmethod
    def compile_clause(node):
        test = node.test
        if isinstance(test, list):
            pass
        else:
            if isinstance(test, ast.BoolOp):
                print ast_helpers.parse_bool(test)
            elif isinstance(test, ast.Compare):
                print test.__dict__
                pass
        return "test"
