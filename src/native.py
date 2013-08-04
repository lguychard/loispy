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
        procname = self.aliases[0] if self.aliases else func.__name__
        proc = type(procname, (NativeProcedure,), {"__call__": func})()
        native[procname] = proc
        for a in self.aliases[1:]:
            native[a] = proc



#-----------------------------
# NATIVE PROCEDURE DEFINITIONS
#-----------------------------

natproc()(min)
natproc()(max)
natproc()(range)
natproc()(map)
natproc()(reduce)
natproc()(filter)
natproc("proc?")(op.isCallable)
natproc()(sys.exit)

@natproc
def error(msg=""):
    raise Error(msg)

@natproc("*")
def multiply(self, *args):
    return reduce(op.mul, args)

@natproc("eq?", "=")
def equals(self, *args):
    return op.eq(*args)

@natproc("-")
def substract(self, *args):
    return reduce(op.sub, args)

@natproc("neq?", )
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

@natproc
def cons(x, y):
    return  [x] + y

@natproc("true?")
def is_true(x):
    return  x == True

@natproc("false?")
def is_false(x):
    return  not x

@natproc("empty?")
def is_empty(x):
    return  not len(x)

@natproc("null?")
def null(x):
    return  x is None

@natproc
def nth(obj, idx):
    return  obj[idx]

@natproc
def last(obj):
    return  obj[-1]

@natproc
def first(obj):
    return  obj[0]

@natproc
def list(*args):
    return  list(args)

@natproc
def car(x):
    return  x[0]

@natproc
def cdr(x):
    return x[1:]
