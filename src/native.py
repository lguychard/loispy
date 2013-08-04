import operator as op
import sys



# ----------------------------------------------------------
# GLOBAL NATIVE: A DICT OF BUILT-IN PROCEDURES AND CONSTANTS
# ----------------------------------------------------------

native = {}



# ---------------
# UTILITY CLASSES
# ---------------


class Error(Exception):
    pass


class NativeProcedure(object):

    def __str__(self):
        return "<Native Procedure %s>" % self.__class__.__name__

    __repr__ = __str__


class natproc(object):

    def __init__(self, *aliases):
        self.aliases = aliases

    def __call__(self, func):
        proc = type(func.__name__, (NativeProcedure,), {"__call__": func})()
        native[func.__name__] = proc
        for a in self.aliases:
            native[a] = proc



#-----------------------------
# NATIVE PROCEDURE DEFINITIONS
#-----------------------------


@natproc
def error(msg=""):
    raise Error(msg)

@natproc
def exit(code=0):
    sys.exit(code)

@natproc("*")
def multiply(self, *args):
    return reduce(op.mul, args)

@natproc("=", "eq?")
def equals(self, *args):
    return op.eq(*args)

@natproc("-")
def substract(self, *args):
    return reduce(op.sub, args)

@natproc("!=", "neq?")
def not_equals(self, *args):
    return op.__ne__(*args)

@natproc("+")
def add(self, *args):
    return reduce(op.add, args)

@natproc("/")
def divide(self, *args):
    return reduce(op.div, args)

@natproc("not")
def logical_not(self, pred):
    return not pred

@natproc("and")
def logical_and(self, *args):
    return all(args)

@natproc("or")
def logical_or(self, *args):
    return any(args)

@natproc("max")
def max(*args): return max(args)


# native = {
#     "#t": True,
#     "#f": False,
#     "#n": None,
#     "*": multiply,
#     "+": add,
#     "=": equals,
#     "-": substract,
#     # "eq?": op.eq,
#     "!=": not_equals,
#     "/": divide(),
#     "not": logical_not,
#     "or": logical_or,
#     "and": logical_and,
#     "max": max,
#     "min": min,
#     "map": map,
#     "reduce": reduce,
#     "filter": filter,
#     "proc?": op.isCallable,
#     "cons": lambda x, y: [x] + y,
#     "exit": exit,
#     "range": range,
#     "true?": lambda x: x == True,
#     "false?": lambda x: not x,
#     "empty?": lambda x: not len(x),
#     "null?": lambda x: x is None,
#     "nth": lambda obj, idx: obj[idx],
#     "last": lambda obj: obj[-1],
#     "first": lambda obj: obj[0],
#     "list": lambda *args: list(args),
#     "car": lambda x: x[0],
#     "cdr": lambda x: x[1:],
#     "error": error
# }