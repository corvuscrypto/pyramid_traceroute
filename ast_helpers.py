import ast

def node_to_string(node):
    if isinstance(node, ast.Str):
        return node.s
    elif isinstance(node, ast.BoolOp):
        return parse_bool(node)
    elif isinstance(node, ast.Compare):
        return parse_compare(node)
    elif isinstance(node, ast.In):
        return "in"
    elif isinstance(node, ast.And):
        return " and "
    elif isinstance(node, ast.Eq):
        return " == "
    elif isinstance(node, ast.Lt):
        return " < "
    elif isinstance(node, ast.Gt):
        return " > "
    elif isinstance(node, ast.GtE):
        return " >= "
    elif isinstance(node, ast.LtE):
        return " <= "
    elif isinstance(node, ast.Or):
        return " or "
    elif isinstance(node, ast.If):
        return "if"
    elif isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Num):
        return str(node.n)
    elif isinstance(node, ast.Call):
        return node.func.id +"("+", ".join([node_to_string(x) for x in node.args])+")"
    return str(node.__class__)
def parse_bool(node):
    strings = []
    op = node_to_string(node.op)
    def to_text(v):
        if isinstance(v, ast.Compare):
            return parse_compare(v)
        elif isinstance(v, ast.BoolOp):
            return "("+parse_bool(v)+")"
        else:
            return node_to_string(v)
    for val in node.values:
        strings.append(to_text(val))
    return op.join(strings)

def parse_compare(node):
    strings = []
    ops = []
    for op in node.ops:
        ops.append(node_to_string(op))
    def to_text(v):
        if isinstance(v, ast.Compare):
            return parse_compare(v)
        elif isinstance(v, ast.BoolOp):
            return parse_bool(v)
        else:
            return node_to_string(v)
    strings.append(to_text(node.left))
    for val in node.comparators:
        strings.append(to_text(val))
    result = strings[0]
    for i in range(len(ops)):
        result += ops[i]+strings[i+1]
    return result
