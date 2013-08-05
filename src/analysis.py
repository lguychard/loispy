from parsing import Symbol, Sym, parse
from environment import Environment
from procedure import Procedure


# 
# ANALYSIS AND EXECUTION
# 


def _eval(_str, env):
    return [analyze(e)(env) for e in parse(_str)]


def analyze(exp):
    if self_eval(exp):
        return lambda env: exp
    elif type(exp) == Symbol:
        return lambda env: env.find(exp)[exp]
    elif type(exp) == list:
        if is_if(exp):
            return analyze_if(exp)
        elif is_begin(exp):
            return analyze_begin(exp)
        elif is_let(exp):
            return analyze_let(exp)
        elif is_lambda(exp):
            return analyze_lambda(exp)
        elif is_def(exp):
            return analyze_def(exp)
        elif is_macrodef(exp):
            return analyze_macrodef(exp)
        elif is_cond(exp):
            return expand_cond(exp)
        elif is_quoted(exp):
            return quotation(exp)
        elif is_getter(exp):
            return analyze_getter(exp)
        else:
            return analyze_procedure_application(exp)
    else:
        raise TypeError("Unknown expression type: %s, %s" % (str(type(exp)), exp))


# 
# EXPRESSION TYPE PREDICATES
# 


def self_eval(exp): return type(exp) in [int, bool, str, float, type(None)]
def is_tagged(exp, tag): return type(exp) == list and exp[0] == Sym(tag)
def is_begin(exp): return is_tagged(exp, "begin")
def is_if(exp): return is_tagged(exp, "if")
def is_let(exp): return is_tagged(exp, "let")
def is_def(exp):return is_tagged(exp, "define")
def is_macrodef(exp):return is_tagged(exp, "define-macro")
def is_cond(exp): return is_tagged(exp, "cond")
def is_proc_applicaton(exp): return type(exp[0]) == Symbol
def is_lambda(exp): return is_tagged(exp, "lambda")
def is_quoted(exp): return is_tagged(exp, "quote")
def is_getter(exp): return type(exp[0]) == Symbol and Sym(exp[0])[0] == "."



# 
# TREATING EXPRESSIONS
# 


def analyze_begin(exp):
    exps = [analyze(e) for e in exp[1:]]
    def seq_noreturn(env):
        for e in exps:
            e(env)


def analyze_if(exp):
    pred = analyze(exp[1])
    then = analyze(exp[2])
    alt = analyze(exp[3]) if len(exp) == 4 else lambda env: False
    return make_if(pred, then, alt)


def make_if(pred, then, alt):
    return lambda env: then(env) if pred(env) else alt(env)


def analyze_let(exp):
    if not len(exp[1]) or not all([len(e) == 2 for e in exp[1]]):
        raise SyntaxError("Invalid vars for let: %s" % exp[1])
    _vars = dict(exp[1])
    exps = analyze_sequence(exp[2:])
    return lambda env: exps(Environment(_vars, env))


def analyze_sequence(seq):
    exps = [analyze(e) for e in seq]
    last = exps.pop()
    def seq(env):
        for e in exps:
            e(env)
        return last(env)
    return seq


def analyze_def(exp):
    if type(exp[1]) == list:
        var, args, body = exp[1][0], exp[1][1:], exp[2:]
        val = make_proc(args, body, name=var)
    else:
        var, val = exp[1], analyze(exp[2])
    return lambda env: env.set(var, val(env))


def analyze_lambda(exp):
    args, body = exp[1], exp[2:]
    return make_proc(args, body)


def make_proc(args, body, name="lambda"):
    body = analyze_sequence(body) if len(body) > 1 else analyze(body[0])
    return lambda env: Procedure(env, args, body, name)


def expand_cond(exp):
    first = exp.pop(0)
    if is_tagged(exp, "else"):
        if exp:
            raise SyntaxError("Else clause isn't last: %s" % str(exp))
        return analyze_sequence(first[1:])
    else:
        pred, then = analyze(exp[0]), analyze_sequence(exp[1:])
        return make_if(pred, then, expand_cond(exp))


def analyze_procedure_application(exp):
    proc = exp[0]
    args = [analyze(e) for e in exp[1:]]
    return lambda env: env.find(proc).get(proc)(*[a(env) for a in args])


def quotation(exp):
    text_of_quotation = exp[1]
    return lambda env: text_of_quotation


def analyze_getter(exp):
    attr = Sym(exp[0])[1:]
    obj = analyze(exp[1])
    args = [analyze(a) for a in exp[2:]]
    def _getattr(env):
        try:
            _obj = obj(env)
            _attr = getattr(_obj, attr)
        except AttributeError:
            raise AttributeError("%s '%s' has no field '%s'" % (
                                type(_obj).__name__, _obj, attr))
        if hasattr(_attr, "__call__"): return _attr(*[a(env) for a in args])
        return _attr
    return _getattr
