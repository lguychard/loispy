from symbol import Symbol

def to_string(x):
    if x is True: return "#t"
    elif x is False: return "#f"
    elif x is None: return "#n"
    elif isa(x, int) or isa(x, float): return str(x)
    elif isa(x, Symbol): return x
    elif isa(x, str): return "\"%s\"" % x
    elif isa(x, list): return "(%s)" % " ".join([to_string(y) for y in x])
    elif isinstance(x, Exception): return "%s: %s" % (type(x).__name__, str(x))
    else:
        return str(x)

def isa(x, type_):
    return type(x) is type_