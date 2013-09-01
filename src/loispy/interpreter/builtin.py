import operator as op
import sys
from symbol import Symbol, Sym
from error import error
from utils import to_string
import math


# ------------------------------------------------------
# GLOBAL builtin DICT: BUILT-IN PROCEDURES AND CONSTANTS
# ------------------------------------------------------


builtin = {
    "#t": True,
    "#f": False,
    "#n": None
}



# ---------------
# UTILITY CLASSES
# ---------------


class BuiltInProcedure(object):

    def __init__(self, func):
        self.func = func

    def __str__(self):
        return "<Built-In Procedure %s>" % self.__class__.__name__

    __repr__ = __str__

    def __call__(self, *args):
        return self.func(*args)


class builtinproc(object):
    """
    This class is meant to be instantiated as a decorator.
    """
    def __init__(self, *aliases):
        self.aliases = aliases

    def __call__(self, func):
        procname = self.aliases[0] if self.aliases else func.__name__
        proc = type(procname, (BuiltInProcedure,), {})(func)
        builtin[procname] = proc
        for a in self.aliases[1:]:
            builtin[a] = proc
        return proc



#-------------------------------
# BUILT-IN PROCEDURE DEFINITIONS
#-------------------------------


for p in len, min, max, range, map, reduce, filter, sys.exit, error:
    builtinproc()(p)


builtinproc("proc?")(op.isCallable)


@builtinproc("*")
def multiply(*args):
    if not len(args) > 1:
        return error("Expected at least 2 arguments, got %d" % len(args))
    else:
        return reduce(op.mul, args)


@builtinproc("eq?", "=")
def equals(*args):
    if not len(args) == 2:
        return error("Expected 2 arguments, got %d" % len(args))
    else:
        return op.eq(*args)

@builtinproc("-")
def substract(*args):
    if not len(args) > 1:
        return error("Expected at least 2 arguments, got %d" % len(args))
    else:
        return reduce(op.sub, args)

@builtinproc("neq?", "!=")
def not_equals(*args):
    assert len(args) == 2, "Expected 2 arguments, got %d" % len(args)
    return op.__ne__(*args)

@builtinproc("+")
def add(*args):
    assert len(args) > 1, "Expected at least 2 arguments, got %d" % len(args)
    return reduce(op.add, args)

@builtinproc("/")
def divide(*args):
    assert len(args) > 1, "Expected at least 2 arguments, got %d" % len(args)
    return reduce(op.div, args)

@builtinproc("not")
def logical_not(pred):
    return not pred

@builtinproc("and")
def logical_and(*args):
    if len(args) == 1 and type(args[0]) is list:
        return all(map(lambda a: a is True, args[0]))
    elif len(args) > 1:
        return all(map(lambda a: a is True, args))
    else:
        raise ValueError("Wrong number of arguments for and (%d)" % len(args))

@builtinproc("or")
def logical_or(*args):
    assert len(args) > 1, "Expected at least 2 arguments, got %d" % len(args)
    return any(args)

@builtinproc("true?")
def is_true(x):
    return x == True

@builtinproc("false?")
def is_false(x):
    return not x

@builtinproc("empty?")
def is_empty(x):
    return not len(x)

@builtinproc("none?")
def null(x):
    return x is None

@builtinproc("even?")
def even(x):
    return not x % 2

@builtinproc("odd?")
def odd(x):
    return bool(x % 2)

@builtinproc("print")
def print_(*data):
    print " ".join([to_string(x) for x in data])

@builtinproc("make-symbol")
def make_symbol(_str):
    return Sym(_str)


# ----------------------
# Manipulating iterables
# ----------------------


@builtinproc()
def nth(lst, idx):
    return lst[idx]

@builtinproc()
def last(lst):
    return lst[-1]

@builtinproc()
def first(lst):
    return lst[0]

@builtinproc("take-from")
def take_from(lst, idx):
    return lst[idx:]

@builtinproc("take-until")
def take_until(lst, idx):
    return lst[:idx]

@builtinproc("all-but-last")
def all_but_last(lst):
    return lst[:len(lst) - 1]

@builtinproc("all-but-first")
def all_but_first(lst):
    return lst[1:]

@builtinproc("list")
def list_(*args):
    return list(args) if args else []

@builtinproc("contains?")
def contains(x, y):
    return y in x


# ------------------
# MANIPULATING DICTS
# ------------------

@builtinproc()
def get(dct, key):
    if type(dct) is not dict:
        raise TypeError("%s... is not a dict" % to_string(dct)[:15])
    return dct[key]

@builtinproc("set-val")
def set_val(dct, key, val):
    if type(dct) is not dict:
        raise TypeError("%s... is not a dict" % to_string(dct)[:15])
    dct[key] = val

@builtinproc()
def keys(dct):
    if type(dct) is not dict:
        raise TypeError("%s... is not a dict" % to_string(dct)[:15])
    return dct.keys()

@builtinproc()
def values(dct):
    if type(dct) is not dict:
        raise TypeError("%s... is not a dict" % to_string(dct)[:15])
    return dct.values()

@builtinproc()
def items(dct):
    if type(dct) is not dict:
        raise TypeError("%s... is not a dict" % to_string(dct)[:15])
    return dct.items()



# ------------------------------------
# TYPE PREDICATES - mutually exclusive
# ------------------------------------


@builtinproc("type")
def type_(arg):
    return type(arg)

@builtinproc("list?")
def is_list(arg):
    return type(arg) is list

@builtinproc("dict?")
def is_dict(arg):
    return type(arg) is dict

@builtinproc("symbol?")
def is_symbol(arg):
    return type(arg) is Symbol

@builtinproc("int?")
def is_int(arg):
    return type(arg) is int

@builtinproc("float?")
def is_float(arg):
    return type(arg) is float

@builtinproc("string?")
def is_str(arg):
    return type(arg) is str

@builtinproc("boolean?")
def is_boolean(arg):
    return type(arg) is bool

@builtinproc("none?")
def is_none(arg):
    return type(arg) is type(None)
