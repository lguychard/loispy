import operator as op
import sys


class Environment(dict):

    def __init__(self, _vars={}, outer=None):
        self.update(_vars)
        self.outer = outer

    def find(self, var):
        if var in self:
            return self
        elif not self.outer:
            raise NameError("%s undefined in current scope" % var)
        else:
            return self.outer.find(var)

    def set(self, var, val):
        self[var] = val


def make_global_env():
    return Environment(native)


native = {
    "#t": True,
    "#f": False,
    "#n": None,
    "*": lambda *args: reduce(op.mul, args),
    "+": lambda *args: reduce(op.add, args),
    "=": op.eq,
    "eq?": op.eq,
    "!=": op.__ne__,
    "/": lambda *args: reduce(op.div, args),
    "not": op.not_,
    "or": lambda *args: any(args),
    "and": lambda *args: all(args),
    "max": max,
    "min": min,
    "map": map,
    "reduce": reduce,
    "filter": filter,
    "proc?": op.isCallable,
    "cons": lambda x, y: [x] + y,
    "exit": lambda: sys.exit(0),
    "range": range,
    "true?": lambda x: x == True,
    "false?": lambda x: not x,
    "empty?": lambda x: not len(x),
    "null?": lambda x: x is None,
    "nth": lambda obj, idx: obj[idx],
    "last": lambda obj: obj[-1],
    "first": lambda obj: obj[0],
    "list": lambda *args: list(args),
    "car": lambda x: x[0],
    "cdr": lambda x: x[1:]
}
