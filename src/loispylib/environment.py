import operator as op

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


native_procs = {
    "*": op.mul,
    "+": op.add,
    "=": op.eq,
    "eq?": op.eq,
    "!=": op.__ne__,
    "/": op.div,
    "not": op.not_,
    "or": any,
    "and": all,
    "max": max,
    "min": min,
    "map": map,
    "reduce": reduce,
    "filter": filter,
    "proc?": op.isCallable,
    "cons": lambda x, y: [x] + y,
    "list": lambda *args: list(args)
}

def make_global_env():
    return Environment(native_procs)