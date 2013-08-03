from parsing import Symbol, Sym
from environment import Environment

def analyze(exp):
    if self_eval(exp): return lambda env: exp
    elif type(exp) == Symbol: return lambda env: env.find(exp)[exp]
    elif is_if(exp): return analyze_if(exp)
    elif is_begin(exp): return analyze_begin(exp)



def self_eval(exp):
    return type(exp) in [int, bool, str, float]

def is_tagged(exp, tag):
    return type(exp) == list and exp[0] == Sym(tag)

def is_begin(exp): return is_tagged(exp, "begin")
def is_if(exp): return is_tagged(exp, "if")
def is_let(exp): return is_tagged(exp, "let")
def is_def(exp): return is_tagged(exp, "def")
def is_cond(exp): return is_tagged(exp, "cond")


def analyze_begin(exp):
    raise NotImplementedError


def analyze_if(exp):
    pred = analyze(exp[1])
    then = analyze(exp[2])
    alt = analyze(exp[3]) if len(exp) == 4 else lambda env: False
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