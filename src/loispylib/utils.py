from parsing import Symbol

def to_string(x):
    if x is True: return "#t"
    elif x is False: return "#f"
    elif type(x) in [int, float]: return str(x)
    elif type(x) == Symbol: return x
    elif type(x) == str: return "\"%s\"" % x
    elif type(x) == list: return "(%s)" % "".join([to_string(y) for y in x])
    else:
        return str(x)
