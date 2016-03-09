import ast

def node_to_string(node):
    if isinstance(node, ast.Str):
        return node.s
    elif isinstance(node, ast.In):
        return "in"
    elif isinstance(node, ast.And):
        return " and "
    elif isinstance(node, ast.Eq):
        return " == "
    elif isinstance(node, ast.Or):
        return " or "
    elif isinstance(node, ast.If):
        return "if"
    elif isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Num):
        return str(node.n)
    elif isinstance(node, ast.Call):
        return node.func.id +"("+", ".join([x for x in node.args])+")"
    return str(node.__class__)
def parse_bool(node):
    strings = []
    op = node_to_string(node.op)
    def to_text(v):
        if isinstance(val, ast.Compare):
            return parse_compare(v)
        elif isinstance(val, ast.BoolOp):
            return "("+parse_bool(v)+")"
        else:
            return node_to_string(v)
    for val in node.values:
        strings.append(to_text(val))
    return op.join(strings)

def parse_compare(node):
    strings = []
    op = node_to_string(node.ops[0])
    def to_text(v):
        if isinstance(v, ast.BoolOp):
            return parse_bool(v)
        else:
            return node_to_string(v)
    strings.append(to_text(node.left))
    for val in node.comparators:
        strings.append(to_text(val))
    return op.join(strings)
