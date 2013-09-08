from symbol import Symbol

def to_string(x):
    if isa(x, bool) or x is None:
        return {True: "#t", False: "#f", None: "#n"}[x]
    elif isa(x, int) or isa(x, float):
        return str(x)
    elif isa(x, Symbol):
        return x
    elif isa(x, str): 
        return "\"%s\"" % x
    elif isa(x, list):
        return "(%s)" % " ".join([to_string(y) for y in x])
    elif isa(x, dict):
        return "{%s}" % " ".join([":%s %s" % (k, to_string(x[k])) for k in x])
    elif isinstance(x, Exception):
        s = "%s: %s" % (type(x).__name__, str(x))
        if hasattr(x, "at"):
            s += "\n    %s" % x.at
        return s
    else:
        return str(x)

def isa(x, type_):
    return type(x) is type_

def add_exc_info(node, e):
    tok = node.tok[:20] + "..." if len(node.tok) > 20 else node.tok
    e.at = "at %s (%d:%d,%d)" % (tok, node.line, node.start, node.end)